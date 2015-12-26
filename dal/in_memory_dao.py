import model

class InMemoryRepo(object):
    def __init__(self):
        print 'Creating in-memory repository'
        self._tasks = {}

    def delete_all_tasks(self):
        self._tasks = {}

    def get_task_by_id(self,task_id):
        return self._tasks[task_id]

    def get_tasks_by_filter(self,filter_dict):
        assignee_predicate = lambda task : (not ('assignee' in filter_dict.keys())) or (task.assignee==filter_dict['assignee'])
        done_predicate = lambda task : (not ('done' in filter_dict.keys())) or (task.done==filter_dict['done'])
        return filter(lambda task : assignee_predicate(task) and done_predicate(task),self._tasks.values())

    # Returns the inserted task_id
    def add_task(self,task):
        self._tasks[task.id] = task
        return task.id

    def mark_task_as_done(self,task_id):
        task = self.get_task_by_id(task_id)
        new_task = model.Task(task.id,task.assignee,task.description,True)
        self._tasks[task_id] = new_task
        return new_task