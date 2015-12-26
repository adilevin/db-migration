import unittest
import tasks_api
import test_api_base

class MongoTestConfig(object):
    ENVIRONMENT = {
            'repository':'mongodb',
            'mongodb_connection_uri' : 'mongodb://localhost:27017/',
            'mongodb_database_name' : 'test'
        }

class TestAPIMongoDB(unittest.TestCase,test_api_base.TestAPI):

  @classmethod
  def setUpClass(cls):
    tasks_api.app.config.from_object(MongoTestConfig)
    tasks_api.connect_db()

  @classmethod
  def tearDownClass(cls):
    tasks_api.disconnect_db()

  def setUp(self):
    self.app = tasks_api.app.test_client()
    tasks_api.clear_db()

  def tearDown(self):
    tasks_api.clear_db()