import unittest
from test_dao_base import TestDAO
from data_access_objects import dao_factory

class TestDAOInMemory(unittest.TestCase,TestDAO):

  def setUp(self):
      self.dao = dao_factory.create_dao({'repository' : 'inmemory'})

  def tearDown(self):
      del(self.dao)
