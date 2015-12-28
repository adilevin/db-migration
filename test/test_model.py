import unittest

from model import task_model


class TestTask(unittest.TestCase):

  def test_task_constructor(self):
      for done in ['False','True']:
          task = task_model.Task('23x4','a','d',done)
          self.assertEqual(task.id,'23x4')
          self.assertEqual(task.assignee,'a')
          self.assertEqual(task.description,'d')
          self.assertEqual(task.done,done)

  def test_task_creation_from_json(self):
      task = task_model.create_task_from_dict(
          {
            'assignee': 'a',
            'description': 'd',
            'done': True,
            'id': '874'
          }
      )
      self.assertEqual(task.assignee,'a')
      self.assertEqual(task.description,'d')
      self.assertEqual(task.id,'874')
      self.assertTrue(task.done)