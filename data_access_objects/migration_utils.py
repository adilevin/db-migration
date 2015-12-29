from model import task_model
from exceptions import TaskIdNotFoundException

def merge_task_collection(favorable_task_list,secondary_task_list):
    # If a task exists in one of the lists, then we return the copy from the favorable list
    merged_tasks = {task.id : task for task in secondary_task_list}
    merged_tasks.update({task.id : task for task in favorable_task_list})
    return merged_tasks.values()

def keep_only_undone_tasks(dao,task_list):
    new_task_list = []
    for t in task_list:
        try:
            if not dao.get_task_by_id(t.id).done:
                new_task_list.append(t)
        except TaskIdNotFoundException:
            new_task_list.append(t)
    return new_task_list
