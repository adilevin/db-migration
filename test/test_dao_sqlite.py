import unittest
from test_dao_base import TestDAO
from data_access_objects import dao_factory

class TestDAOSqlite(unittest.TestCase,TestDAO):

  def setUp(self):
      self.dao = dao_factory.create_dao({
            'repository':'sqlite',
            'sqlite_file_path' : 'sqlite_files/sqlite_test.db',
        })

  def tearDown(self):
      self.dao.delete_all_tasks()
      del(self.dao)

  def expect_task_ids_when_iterating(self,task_ids):
      count = 0
      for t in self.dao.iterate_all_tasks():
          self.assertEqual(t.id,task_ids[count])
          count = count + 1

  def test_iterate_all_tasks(self):
    self.expect_task_ids_when_iterating([])
    id0 = self.add_task('a1','d1')
    id1 = self.add_task('a1','d1')
    self.dao.mark_task_as_done(id1)
    self.expect_task_ids_when_iterating([id0,id1])