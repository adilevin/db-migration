from pymongo import MongoClient
import tasks_api

class Mongo(object):
    def __init__(self,connection_uri,database_name):
        print 'Connecting to %s' % connection_uri
        self.database_name = database_name
        self.client = MongoClient(connection_uri)
        print '  Using database "%s"' % database_name
        self.db = self.client[database_name]
        print '  Using collection "tasks"'
        self.collection = self.db.tasks

    def clear(self):
        if self.database_name!='test':
            raise 'Only the test database is allowed to be cleared'
        count = self.collection.delete_many({}).deleted_count
