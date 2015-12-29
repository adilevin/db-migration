
class TaskIdNotFoundException(Exception):

    def __init__(self, task_id):
        self.task_id = task_id

    def __str__(self):
        return repr('Task %s was not found' + self.task_id)