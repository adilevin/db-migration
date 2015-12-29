import unittest

from data_access_objects import migration_utils
from model.task_model import Task

class TestMigrationUtils(unittest.TestCase):

  def test_trivial_merge_of_task_lists(self):
      task_list_0 = [Task('id0','a0','d0',False),Task('id1','a1','d1',True)]
      merged_task_list = migration_utils.merge_task_collection(task_list_0,[])
      self.assertTrue(set(merged_task_list)==set(task_list_0))
      merged_task_list = migration_utils.merge_task_collection([],task_list_0)
      self.assertTrue(set(merged_task_list)==set(task_list_0))

  def test_merge_of_identical_task_lists(self):
      task_list_0 = [Task('id0','a0','d0',False),Task('id1','a1','d1',True)]
      merged_task_list = migration_utils.merge_task_collection(task_list_0,task_list_0)
      self.assertTrue(set(merged_task_list)==set(task_list_0))

  def test_merge_of_complementary_task_lists(self):
      t = [Task('id0','a0','d0',False),Task('id1','a1','d1',True)]
      merged_list = migration_utils.merge_task_collection([t[0]],[t[1]])
      self.assertTrue(set(merged_list)==set(t))

  def test_merge_of_overlapping_task_lists(self):
      t = [Task('id0','a0','d0',False),Task('id1','a1','d1',True),Task('id2','a2','d2',True)]
      merged_list = migration_utils.merge_task_collection([t[0],t[1]],[t[0],t[2]])
      self.assertTrue(set(merged_list)==set(t))

  def test_favoring_of_the_first_list(self):
      merged_list = migration_utils.merge_task_collection([Task('id0','a0','d0',False)],[Task('id0','a0','d0',True)])
      self.assertEqual(len(merged_list),1)
      self.assertFalse(merged_list[0].done)
      merged_list = migration_utils.merge_task_collection([Task('id0','a0','d0',True)],[Task('id0','a0','d0',False)])
      self.assertEqual(len(merged_list),1)
      self.assertTrue(merged_list[0].done)
