from model import task_model
from exceptions import TaskIdNotFoundException

class InMemoryRepo(object):
    def __init__(self):
        self._tasks = {}

    def delete_all_tasks(self):
        self._tasks = {}

    def get_task_by_id(self,task_id):
        try:
            return self._tasks[task_id]
        except Exception as e:
            raise TaskIdNotFoundException(task_id)

    def get_all_undone_tasks_for_assignee(self,assignee):
        assignee_predicate = lambda task : (task.assignee==assignee)
        done_predicate = lambda task : (task.done==False)
        return filter(lambda task : assignee_predicate(task) and done_predicate(task),self._tasks.values())

    # Returns the inserted task_id
    def add_task(self,task):
        self._tasks[task.id] = task
        return task.id

    def mark_task_as_done(self,task_id):
        task = self.get_task_by_id(task_id)
        new_task = task_model.Task(task.id,task.assignee,task.description,True)
        self._tasks[task_id] = new_task
        return new_task