import unittest
from test_dao_base import TestDAO
from dal import dao_factory

class TestInMemoryDAO(unittest.TestCase,TestDAO):

  def setUp(self):
      self.dao = dao_factory.create_dao({'repository' : 'inmemory'})

  def tearDown(self):
      del(self.dao)
