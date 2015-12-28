import unittest
from test_dao_base import TestDAO
from data_access_objects import dao_factory

class TestInMemoryDAO(unittest.TestCase,TestDAO):

  def setUp(self):
      self.dao = dao_factory.create_dao({
            'repository':'sqlite',
            'sqlite_file_path' : 'sqlite_files/sqlite_test.db',
        })

  def tearDown(self):
      self.dao.delete_all_tasks()
      del(self.dao)


