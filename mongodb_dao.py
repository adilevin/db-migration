from pymongo import MongoClient, ReturnDocument
import model

def _mongo_dict_to_task(mongo_dict):
    task_as_dict = dict(mongo_dict)
    task_as_dict['id'] = task_as_dict['_id']
    task_as_dict.pop('_id')
    return model.create_task_from_dict(task_as_dict)


class Mongo(object):
    def __init__(self,connection_uri,database_name):
        print 'Connecting to %s' % connection_uri
        self.database_name = database_name
        self.client = MongoClient(connection_uri)
        print '  Using database "%s"' % database_name
        self.db = self.client[database_name]
        print '  Using collection "tasks"'
        self._collection = self.db.tasks

    def clear(self):
        if self.database_name!='test':
            raise 'Only the test database is allowed to be cleared'
        count = self._collection.delete_many({}).deleted_count

    def get_task_by_id(self,task_id):
        task_as_dict = self._collection.find_one(filter = {'_id':task_id})
        return _mongo_dict_to_task(task_as_dict)

    def get_tasks_by_filter(self,filter):
        cursor = self._collection.find(filter)
        tasks = [_mongo_dict_to_task(x) for x in cursor]
        return tasks

    # Returns the inserted task_id
    def add_task(self,task):
        result = self._collection.insert_one({'_id':task.id,'assignee':task.assignee,'description':task.description,'done':task.done});
        return result.inserted_id

    def mark_task_as_done(self,task_id):
        doc = self._collection.find_one_and_update(filter={'_id':task_id},update={'$set': {'done':True}},
            return_document=ReturnDocument.AFTER)
        return _mongo_dict_to_task(doc)