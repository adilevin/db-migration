from model import task_model

def merge_task_collection(favorable_task_list,secondary_task_list):
    # If a task exists in one of the lists, then we return the copy from the favorable list
    merged_tasks = {task.id : task for task in secondary_task_list}
    merged_tasks.update({task.id : task for task in favorable_task_list})
    return merged_tasks.values()
