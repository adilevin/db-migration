import json

class TestAPI(object):

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
    task_id = json.loads(rv.data)['id']
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

  def get_all_tasks_for_assignee(self,assignee):
    rv = self.app.get('/tasks?assignee=%s' % assignee)
    self.assertEqual(rv.status_code,200)
    return json.loads(rv.data)

  def get_all_undone_tasks_for_assignee(self,assignee):
    rv = self.app.get('/tasks?assignee=%s&done=False' % assignee)
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

  def test_get_multiple_tasks(self):
    for i in range(3):
        self.add_task('a1','d1')
    for i in range(2):
        self.add_task('a2','d2')
    self.assertEqual(len(self.get_all_tasks_for_assignee('a1')),3)
    self.assertEqual(len(self.get_all_tasks_for_assignee('a2')),2)
    self.assertEqual(len(self.get_all_tasks()),5)
    task_id = self.add_task('a1','d1')
    self.assertEqual(len(self.get_all_undone_tasks_for_assignee('a1')),4)
    self.mark_task_as_done(task_id)
    self.assertEqual(len(self.get_all_undone_tasks_for_assignee('a1')),3)


  def test_mark_task_as_done(self):
      task_id = self.add_task('a','d')
      task = self.get_task(task_id)
      self.assertFalse(task['done'])
      self.mark_task_as_done(task_id)
      task = self.get_task(task_id)
      self.assertTrue(task['done'])
