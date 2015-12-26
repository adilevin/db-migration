import tasks_api

class Mongo(object):
    def __init__(self,connection_uri,database_name):
        from pymongo import MongoClient
        self.client = MongoClient(connection_uri)
        self.db = self.client[database_name]
        self.collection = self.db.tasks
