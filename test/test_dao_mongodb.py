import unittest
from test_dao_base import TestDAO
from data_access_objects import dao_factory

class TestDAOMongoDB(unittest.TestCase,TestDAO):

  def setUp(self):
      self.dao = dao_factory.create_dao({
            'repository':'mongodb',
            'mongodb_connection_uri' : 'mongodb://localhost:27017/',
            'mongodb_database_name' : 'test'
        })

  def tearDown(self):
      self.dao.delete_all_tasks()
      del(self.dao)