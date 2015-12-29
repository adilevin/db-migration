import unittest
from test_dao_base import TestDAO
from data_access_objects import dao_factory

def create_data_access_object(step):
    return dao_factory.create_dao({
            'repository':'migrate_from_sqlite_to_mongodb',
            'mongodb_connection_uri' : 'mongodb://localhost:27017/',
            'mongodb_database_name' : 'test',
            'sqlite_file_path' : 'sqlite_files/sqlite_test.db',
            'migration_step' : step
        })


class TestMigrationStep2(unittest.TestCase,TestDAO):

  def setUp(self):
      self.dao = create_data_access_object(2)

  def tearDown(self):
      self.dao.delete_all_tasks()
      del(self.dao)

class TestMigrationStep3(unittest.TestCase,TestDAO):

  def setUp(self):
      self.dao = create_data_access_object(3)

  def tearDown(self):
      self.dao.delete_all_tasks()
      del(self.dao)

class TestMigrationStep4(unittest.TestCase,TestDAO):

  def setUp(self):
      self.dao = create_data_access_object(4)

  def tearDown(self):
      self.dao.delete_all_tasks()
      del(self.dao)


class TestMigrationStep5(unittest.TestCase,TestDAO):

  def setUp(self):
      self.dao = create_data_access_object(5)

  def tearDown(self):
      self.dao.delete_all_tasks()
      del(self.dao)

class TestMigrationStep6(unittest.TestCase,TestDAO):

  def setUp(self):
      self.dao = create_data_access_object(6)

  def tearDown(self):
      self.dao.delete_all_tasks()
      del(self.dao)

class TestMigrationStep7(unittest.TestCase,TestDAO):

  def setUp(self):
      self.dao = create_data_access_object(7)

  def tearDown(self):
      self.dao.delete_all_tasks()
      del(self.dao)
