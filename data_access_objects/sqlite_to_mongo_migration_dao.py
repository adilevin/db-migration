import sqlite3

from model import task_model
from migration_utils import merge_task_collection
import mongodb_dao, sqlite_dao
from exceptions import TaskIdNotFoundException

# Step 2: Ignore the new DB. Purpose: Test new DB in test environments.
# Step 3: Write to old DB first, then to new DB. Read from the old DB. Purpose: Test new write path.
# Step 4: Write to old DB first, then to new DB. Read from both. Purpose: Test new read path.
#  In step 5 we write to a fresh new database. Not on top of what we had in step 4.
# Step 5: Write to new DB first, then to old DB. Read from both. Purpose: Make the new DB the consistent one.
#   When reading, we need to know for each record whether it has been written in step 5 or prior to it.
#   If it is written in step 5, then it is in authoritative state. Otherwise it isn't.
# Step 6: Stop writing to the old DB. Read from both.
# Step 7: Migrate old data from the old DB to the new DB.
# Step 8: Write and read only to new DB.

class MigrationDAO(object):
    def __init__(self,config):
        self.old_db = sqlite_dao.SQLiteRepo(config['sqlite_file_path'])
        self.new_db = mongodb_dao.Mongo(
            connection_uri=config['mongodb_connection_uri'],
            database_name=config['mongodb_database_name'])
        self.migration_feature_toggle = config['migration_feature_toggle']

    def delete_all_tasks(self):
        self.old_db.delete_all_tasks()
        self.new_db.delete_all_tasks()

    def get_task_by_id(self,task_id):
        if self.migration_feature_toggle in [2,3]:
            return self.old_db.get_task_by_id(task_id)
        if self.migration_feature_toggle==4:
            try:
                return self.new_db.get_task_by_id(task_id)
            except TaskIdNotFoundException:
                return self.old_db.get_task_by_id(task_id)

    def get_all_undone_tasks_for_assignee(self,assignee):
        if self.migration_feature_toggle in [2,3]:
            return self.old_db.get_all_undone_tasks_for_assignee(assignee)
        if self.migration_feature_toggle==4:
            tasks_from_old_db = self.old_db.get_all_undone_tasks_for_assignee(assignee)
            tasks_from_new_db = self.new_db.get_all_undone_tasks_for_assignee(assignee)
            return merge_task_collection(tasks_from_old_db,tasks_from_new_db)

    # Returns the inserted task_id
    def add_task(self,task):
        if self.migration_feature_toggle==2:
            res = self.old_db.add_task(task)
            return res
        if self.migration_feature_toggle in [3,4]:
            res = self.old_db.add_task(task)
            self.new_db.add_task(task)
            return res

    def mark_task_as_done(self,task_id):
        if self.migration_feature_toggle==2:
            res = self.old_db.mark_task_as_done(task_id)
            return res
        if self.migration_feature_toggle in [3,4]:
            res = self.old_db.mark_task_as_done(task_id)
            self.new_db.mark_task_as_done(task_id)
            return res
