from model import task_model
from exceptions import TaskIdNotFoundException

def unite_lists_of_undone_tasks(task_list_0,task_list_1):
    merged_tasks = {task.id : task for task in task_list_0}
    merged_tasks.update({task.id : task for task in task_list_1})
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

def eagerly_migrate_data_from_sqlite_to_mongodb(config):
    from sqlite_dao import SQLiteDAO
    from mongodb_dao import MongoDBDAO
    old_db, new_db = SQLiteDAO(config), MongoDBDAO(config)
    for t in old_db.iterate_all_tasks():
        if not new_db.has_task_with_id(t.id):
            new_db.add_task(t) # t doesn't exist in new DB, so add it
        elif t.done:
            new_db.mark_task_as_done(t.id) # t is marked as done in the old DB, so mark it as done in the new DB
