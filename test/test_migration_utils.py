import unittest

from data_access_objects import migration_utils
from model.task_model import Task

class TestUnitingOfUndoneTasksLists(unittest.TestCase):

  def test_trivial_uniting_of_task_lists(self):
      task_list_0 = [Task('id0','a0','d0',False),Task('id1','a1','d1',False)]
      united_task_list = migration_utils.unite_lists_of_undone_tasks(task_list_0,[])
      self.assertTrue(set(united_task_list)==set(task_list_0))
      united_task_list = migration_utils.unite_lists_of_undone_tasks([],task_list_0)
      self.assertTrue(set(united_task_list)==set(task_list_0))

  def test_merge_of_identical_task_lists(self):
      task_list_0 = [Task('id0','a0','d0',False),Task('id1','a1','d1',False)]
      united_task_list = migration_utils.unite_lists_of_undone_tasks(task_list_0,task_list_0)
      self.assertTrue(set(united_task_list)==set(task_list_0))

  def test_merge_of_complementary_task_lists(self):
      t = [Task('id0','a0','d0',False),Task('id1','a1','d1',False)]
      united_task_list = migration_utils.unite_lists_of_undone_tasks([t[0]],[t[1]])
      self.assertTrue(set(united_task_list)==set(t))

  def test_merge_of_overlapping_task_lists(self):
      t = [Task('id0','a0','d0',False),Task('id1','a1','d1',True),Task('id2','a2','d2',True)]
      united_task_list = migration_utils.unite_lists_of_undone_tasks([t[0],t[1]],[t[0],t[2]])
      self.assertTrue(set(united_task_list)==set(t))


class TestEagerMigrationFromSQLiteToMongoDB(unittest.TestCase):

  def setUp(self):
      self.config = {
            'repository':'migrate_from_sqlite_to_mongodb',
            'mongodb_connection_uri' : 'mongodb://localhost:27017/',
            'mongodb_database_name' : 'test',
            'sqlite_file_path' : 'sqlite_files/sqlite_test.db'
      }
      from data_access_objects import sqlite_dao
      from data_access_objects import mongodb_dao
      self.old_db = sqlite_dao.SQLiteDAO(self.config)
      self.new_db = mongodb_dao.MongoDBDAO(self.config)
      self.old_db.delete_all_tasks()
      self.new_db.delete_all_tasks()

  def tearDown(self):
      self.old_db.delete_all_tasks()
      self.new_db.delete_all_tasks()
      del(self.old_db)
      del(self.new_db)

  def insert_tasks_to_old_db(self):
      self.old_db.add_task(Task('Undone task that exists only in old DB', 'a0', 'd0', False))
      self.old_db.add_task(Task('Done task that exists only in old DB', 'a1', 'd1', True))
      self.old_db.add_task(Task('Task that is undone in the old DB by done in the new DB', 'a2', 'd2', False))
      self.old_db.add_task(Task('Task that is done in the old DB by undone in the new DB', 'a3', 'd3', True))

  def insert_tasks_to_new_db(self):
      self.new_db.add_task(Task('Task that is undone in the old DB by done in the new DB', 'a2', 'd2', True))
      self.new_db.add_task(Task('Task that is done in the old DB by undone in the new DB', 'a3', 'd3', False))

  def verify_expected_tasks_in_new_db(self):
      self.assertFalse(self.new_db.get_task_by_id('Undone task that exists only in old DB').done)
      self.assertTrue(self.new_db.get_task_by_id('Done task that exists only in old DB').done)
      self.assertTrue(self.new_db.get_task_by_id('Task that is undone in the old DB by done in the new DB').done)
      self.assertTrue(self.new_db.get_task_by_id('Task that is done in the old DB by undone in the new DB').done)
      self.assertTrue(type(self.new_db.get_task_by_id('Undone task that exists only in old DB').done)==bool)

  def test_eager_migration_from_sqlite_to_mongodb(self):
      self.insert_tasks_to_old_db()
      self.insert_tasks_to_new_db()
      migration_utils.eagerly_migrate_data_from_sqlite_to_mongodb(self.config)
      self.verify_expected_tasks_in_new_db()