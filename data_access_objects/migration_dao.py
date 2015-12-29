import sqlite3

from migration_utils import merge_task_collection, keep_only_undone_tasks
from exceptions import TaskIdNotFoundException, DBWriteException

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
    def __init__(self,old_db,new_db,migration_step):
        self.old_db = old_db
        self.new_db = new_db
        self.migration_step = migration_step

    def delete_all_tasks(self):
        self.old_db.delete_all_tasks()
        self.new_db.delete_all_tasks()

    def read_from_both_databases(self,task_id):
        task_from_old_db = None
        task_from_new_db = None
        if self.migration_step in [2,3,4]:
            try:
                task_from_old_db = self.old_db.get_task_by_id(task_id)
            except TaskIdNotFoundException:
                pass
        if self.migration_step in [4,5,6]:
            try:
                task_from_new_db = self.new_db.get_task_by_id(task_id)
            except TaskIdNotFoundException:
                pass
        return task_from_old_db, task_from_new_db

    def resolve_task_conflicts(self,old,new):
        if self.migration_step in [2,3,4]:
            return old
        elif self.migration_step==5:
            if new!=None and (old==None or old.timestamp==5):
                return new
            else:
                return old

    def get_task_by_id(self,task_id):
        task_from_old_db, task_from_new_db = self.read_from_both_databases(task_id)
        if task_from_old_db==None and task_from_new_db==None:
            raise TaskIdNotFoundException(task_id)
        return self.resolve_task_conflicts(task_from_old_db,task_from_new_db)

    def resolve_task_collection_conflicts(self,old,new):
        if self.migration_step in [2,3,4]:
            return old
        elif self.migration_step==5:
            merged_task_list = merge_task_collection(old,new)
            merged_task_list = keep_only_undone_tasks(self.old_db,merged_task_list)
            merged_task_list = keep_only_undone_tasks(self.new_db,merged_task_list)
            return merged_task_list

    def get_all_undone_tasks_for_assignee(self,assignee):
        if self.migration_step in [2,3]:
            return self.old_db.get_all_undone_tasks_for_assignee(assignee)
        elif self.migration_step in [4,5]:
            tasks_from_old_db = self.old_db.get_all_undone_tasks_for_assignee(assignee)
            tasks_from_new_db = self.new_db.get_all_undone_tasks_for_assignee(assignee)
            return self.resolve_task_collection_conflicts(tasks_from_old_db,tasks_from_new_db)


    # Returns the inserted task_id
    def add_task(self,task):
        if self.migration_step==2:
            res = self.old_db.add_task(task)
            return res
        elif self.migration_step in [3,4]:
            res = self.old_db.add_task(task)
            try:
                self.new_db.add_task(task)
            except DBWriteException:
                pass
            return res
        elif self.migration_step == 5:
            res = self.new_db.add_task(task)
            try:
                self.old_db.add_task(task)
            except DBWriteException:
                pass
            return res

    def mark_task_as_done(self,task_id):
        if self.migration_step==2:
            res = self.old_db.mark_task_as_done(task_id)
            return res
        elif self.migration_step in [3,4]:
            res = self.old_db.mark_task_as_done(task_id)
            try:
                self.new_db.mark_task_as_done(task_id)
            except DBWriteException:
                pass
            return res
        elif self.migration_step==5:
            res_new = self.new_db.mark_task_as_done(task_id)
            try:
                res_old = self.old_db.mark_task_as_done(task_id)
            except DBWriteException:
                pass
            return res_new