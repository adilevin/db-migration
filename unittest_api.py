import unittest
import tasks_api
import json

def setUpModule():
    tasks_api.app.config.from_pyfile('test_config.py')
    tasks_api.connect_db()

class TestAPI(unittest.TestCase):

  def setUp(self):
    self.app = tasks_api.app.test_client()
    tasks_api.clear_db()

  def tearDown(self):
    tasks_api.clear_db()

  def test_home_path_returns_200(self):
    rv = self.app.get('/')
    self.assertEqual(rv.status_code,200)

  def test_tasks_returns_200(self):
    rv = self.app.get('/tasks')
    self.assertEqual(rv.status_code,200)
    self.assertEqual(rv.data,'[]')

  def add_task(self,assignee,description):
    rv = self.app.post('/tasks',data={
        'assignee':assignee,
        'description':description
    })
    self.assertEqual(rv.status_code,200)
    task_id = json.loads(rv.data)['_id']
    self.assertGreater(len(task_id),20)
    return task_id

  def get_task(self,task_id):
    rv = self.app.get('/tasks/' + str(task_id))
    self.assertEqual(rv.status_code,200)
    return json.loads(rv.data)

  def get_all_tasks(self):
    rv = self.app.get('/tasks')
    self.assertEqual(rv.status_code,200)
    return json.loads(rv.data)

  def mark_task_as_done(self,task_id):
    rv = self.app.put('/tasks/' + str(task_id))
    self.assertEqual(rv.status_code,200)
    return json.loads(rv.data)

  def test_add_tasks(self):
    for i in range(3):
        assignee = 'a' + str(i)
        description = 'd' + str(i)
        task_id = self.add_task(assignee,description)
        task = self.get_task(task_id)
        self.assertEqual(task['assignee'],assignee)
        self.assertEqual(task['description'],description)
        self.assertFalse(task['done'])
    all_tasks = self.get_all_tasks()
    self.assertEqual(len(all_tasks),3)

  def test_mark_task_as_done(self):
      task_id = self.add_task('a','d')
      task = self.get_task(task_id)
      self.assertFalse(task['done'])
      self.mark_task_as_done(task_id)
      task = self.get_task(task_id)
      self.assertTrue(task['done'])

if __name__ == '__main__':
    unittest.main()
