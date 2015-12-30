from pymongo import MongoClient, ReturnDocument, ASCENDING
from pymongo.errors import ServerSelectionTimeoutError
from exceptions import TaskIdNotFoundException
from model import task_model

def _mongo_dict_to_task(mongo_dict):
    task_as_dict = dict(mongo_dict)
    task_as_dict['id'] = task_as_dict['_id']
    task_as_dict.pop('_id')
    return task_model.create_task_from_dict(task_as_dict)

class MongoDBDAO(object):
    def __init__(self,config):
        self.database_name = config['mongodb_database_name']
        self.client = MongoClient(config['mongodb_connection_uri'],serverSelectionTimeoutMS=1000)
        try:
            self.client.server_info()
        except ServerSelectionTimeoutError:
            raise Exception('Failed to connect to MongoDB at %s\nCheck that the connection URI is good and that mongod is running' % connection_uri)
        self.db = self.client[self.database_name]
        self._collection = self.db.tasks
        self._collection.create_index([('assignee',ASCENDING),('done',ASCENDING)]);


    def delete_all_tasks(self):
        if self.database_name!='test':
            raise 'Only the test database is allowed to be cleared'
        count = self._collection.delete_many({}).deleted_count

    def get_task_by_id(self,task_id):
        task_as_dict = self._collection.find_one(filter = {'_id':task_id})
        if task_as_dict==None:
            raise TaskIdNotFoundException(task_id)
        return _mongo_dict_to_task(task_as_dict)

    def has_task_with_id(self,task_id):
        return self._collection.find(filter = {'_id':task_id}).count()>0

    def get_all_undone_tasks_for_assignee(self,assignee):
        cursor = self._collection.find({'assignee':assignee,'done':False})
        tasks = [_mongo_dict_to_task(x) for x in cursor]
        return tasks

    # Returns the inserted task_id
    def add_task(self,task):
        result = self._collection.insert_one({'_id':task.id,'assignee':task.assignee,'description':task.description,'done':task.done});
        return result.inserted_id

    def mark_task_as_done(self,task_id):
        doc = self._collection.find_one_and_update(filter={'_id':task_id},update={'$set': {'done':True}},
            return_document=ReturnDocument.AFTER)
        if doc==None:
            raise TaskIdNotFoundException(task_id)
        return _mongo_dict_to_task(doc)