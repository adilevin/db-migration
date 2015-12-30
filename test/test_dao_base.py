import uuid

from model import task_model
from data_access_objects.exceptions import TaskIdNotFoundException
from data_access_objects import migration_utils

class TestDAO(object):

  def add_task(self,assignee,description,done=False):
    task_id = self.dao.add_task(task_model.Task(str(uuid.uuid4()),assignee,description,done))
    self.assertGreater(len(task_id),20)
    return task_id

  def test_add_and_get_individual_tasks(self):
    for i in range(3):
        assignee = 'a' + str(i)
        description = 'd' + str(i)
        task_id = self.add_task(assignee,description,i%2==0)
        task = self.dao.get_task_by_id(task_id)
        self.assertEqual(task.assignee,assignee)
        self.assertEqual(task.description,description)
        self.assertEqual(task.done,i%2==0)
        self.assertEqual(bool,type(task.done))

  def test_has_task_with_id(self):
    self.assertFalse(self.dao.has_task_with_id('INVALID_ID_FOR_TEST'))
    task_id = self.add_task('a','d')
    self.assertTrue(self.dao.has_task_with_id(task_id))

  def test_get_multiple_tasks(self):
    for i in range(3):
        self.add_task('a1','d1')
    for i in range(2):
        self.add_task('a2','d2')
    self.assertEqual(len(self.dao.get_all_undone_tasks_for_assignee('a1')),3)
    self.assertEqual(bool,type(self.dao.get_all_undone_tasks_for_assignee('a1')[0].done))
    self.assertEqual(len(self.dao.get_all_undone_tasks_for_assignee('a2')),2)
    task_id = self.add_task('a1','d1')
    self.assertEqual(len(self.dao.get_all_undone_tasks_for_assignee('a1')),4)
    self.dao.mark_task_as_done(task_id)
    self.assertEqual(len(self.dao.get_all_undone_tasks_for_assignee('a1')),3)


  def test_mark_task_as_done(self):
      task_id = self.add_task('a','d')
      task = self.dao.get_task_by_id(task_id)
      self.assertFalse(task.done)
      self.dao.mark_task_as_done(task_id)
      task = self.dao.get_task_by_id(task_id)
      self.assertTrue(task.done)

  def test_exception_raised_by_get_task_in_case_task_not_found(self):
      task_id = 'INVALID_TASK_ID'
      try:
        task = self.dao.get_task_by_id(task_id)
        self.fail()
      except TaskIdNotFoundException as e:
          self.assertEquals(e.task_id,task_id)

  def test_exception_raised_by_mark_task_as_done_in_case_task_not_found(self):
      task_id = 'INVALID_TASK_ID'
      try:
        self.dao.mark_task_as_done(task_id)
        self.fail()
      except TaskIdNotFoundException as e:
          self.assertEquals(e.task_id,task_id)

  def test_keep_only_undone_tasks(self):
    for i in range(2):
        self.add_task('a1','d1')
    tasks2 = self.dao.get_all_undone_tasks_for_assignee('a1')
    self.assertEqual(len(tasks2),2)
    task3_id = self.add_task('a1','d1')
    tasks3 = self.dao.get_all_undone_tasks_for_assignee('a1')
    self.assertEqual(len(tasks3),3)
    self.dao.mark_task_as_done(task3_id)
    tasks_remaining = migration_utils.keep_only_undone_tasks(self.dao,tasks3)
    self.assertTrue(set(tasks_remaining)==set(tasks2))