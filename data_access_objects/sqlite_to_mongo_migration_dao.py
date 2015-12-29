import sqlite3

from model import task_model
from migration_utils import merge_task_collection
import mongodb_dao, sqlite_dao
from exceptions import TaskIdNotFoundException

class MigrationDAO(object):
    def __init__(self,config):
        self.old_dao = sqlite_dao.SQLiteRepo(config['sqlite_file_path'])
        self.new_dao = mongodb_dao.Mongo(
            connection_uri=config['mongodb_connection_uri'],
            database_name=config['mongodb_database_name'])
        self.migration_feature_toggle = config['migration_feature_toggle']

    def delete_all_tasks(self):
        self.old_dao.delete_all_tasks()
        self.new_dao.delete_all_tasks()

    def get_task_by_id(self,task_id):
        if self.migration_feature_toggle in [2,3]:
            return self.old_dao.get_task_by_id(task_id)
        if self.migration_feature_toggle==4:
            try:
                return self.new_dao.get_task_by_id(task_id)
            except TaskIdNotFoundException:
                return self.old_dao.get_task_by_id(task_id)

    def get_tasks_by_filter(self,filter_dict):
        if self.migration_feature_toggle in [2,3]:
            return self.old_dao.get_tasks_by_filter(filter_dict)
        if self.migration_feature_toggle==4:
            tasks_from_old_db = self.old_dao.get_tasks_by_filter(filter_dict)
            tasks_from_new_db = self.new_dao.get_tasks_by_filter(filter_dict)
            return merge_task_collection(tasks_from_old_db,tasks_from_new_db)

    # Returns the inserted task_id
    def add_task(self,task):
        if self.migration_feature_toggle==2:
            res = self.old_dao.add_task(task)
            return res
        if self.migration_feature_toggle in [3,4]:
            res = self.old_dao.add_task(task)
            self.new_dao.add_task(task)
            return res

    def mark_task_as_done(self,task_id):
        if self.migration_feature_toggle==2:
            res = self.old_dao.mark_task_as_done(task_id)
            return res
        if self.migration_feature_toggle in [3,4]:
            res = self.old_dao.mark_task_as_done(task_id)
            self.new_dao.mark_task_as_done(task_id)
            return res
