import json
from collections import namedtuple

Task = namedtuple('Task','id assignee description done')

def obj_to_json(obj):
    return json.dumps(obj.__dict__)

def array_to_json(arr):
    return json.dumps([item.__dict__ for item in arr])

def mark_as_done(task):
    return Task(id=task.id, assignee=task.assignee, description=task.description, done=True)

def create_task_from_dict(task_as_dict):
    return Task(**task_as_dict)