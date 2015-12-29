import uuid

from model import task_model
from data_access_objects.exceptions import TaskIdNotFoundException

class TestDAO(object):

  def add_task(self,assignee,description):
    task_id = self.dao.add_task(task_model.Task(str(uuid.uuid4()),assignee,description,False))
    self.assertGreater(len(task_id),20)
    return task_id

  def get_all_tasks_for_assignee(self,assignee):
    return self.dao.get_tasks_by_filter({'assignee':assignee})

  def get_all_undone_tasks_for_assignee(self,assignee):
    return self.dao.get_tasks_by_filter({'assignee':assignee,'done':False})

  def test_add_tasks(self):
    for i in range(3):
        assignee = 'a' + str(i)
        description = 'd' + str(i)
        task_id = self.add_task(assignee,description)
        task = self.dao.get_task_by_id(task_id)
        self.assertEqual(task.assignee,assignee)
        self.assertEqual(task.description,description)
        self.assertFalse(task.done)

  def test_get_multiple_tasks(self):
    for i in range(3):
        self.add_task('a1','d1')
    for i in range(2):
        self.add_task('a2','d2')
    self.assertEqual(len(self.get_all_tasks_for_assignee('a1')),3)
    self.assertEqual(len(self.get_all_tasks_for_assignee('a2')),2)
    self.assertEqual(len(self.dao.get_tasks_by_filter({})),5)
    task_id = self.add_task('a1','d1')
    self.assertEqual(len(self.get_all_undone_tasks_for_assignee('a1')),4)
    self.dao.mark_task_as_done(task_id)
    self.assertEqual(len(self.get_all_undone_tasks_for_assignee('a1')),3)


  def test_mark_task_as_done(self):
      task_id = self.add_task('a','d')
      task = self.dao.get_task_by_id(task_id)
      self.assertFalse(task.done)
      self.dao.mark_task_as_done(task_id)
      task = self.dao.get_task_by_id(task_id)
      self.assertTrue(task.done)

  def test_exception_raised_in_case_task_not_found(self):
      task_id = 'INVALID_TASK_ID'
      try:
        task = self.dao.get_task_by_id(task_id)
      except TaskIdNotFoundException as e:
          self.assertEquals(e.task_id,task_id)