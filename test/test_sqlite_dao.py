import unittest
from test_dao_base import TestDAO
from dal import dao_factory

class TestInMemoryDAO(unittest.TestCase,TestDAO):

  def setUp(self):

      self.dao = dao_factory.create_dao({
            'repository':'sqlite',
            'sqlite_file_path' : 'sqlite_test.db',
        })

  def tearDown(self):
      self.dao.delete_all_tasks()
      del(self.dao)


