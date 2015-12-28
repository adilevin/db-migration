import unittest

from main import tasks_api
import test_api_base


class InMemoryTestConfig(object):
    ENVIRONMENT = {
            'repository' : 'inmemory',
        }

class TestAPIInMemory(unittest.TestCase,test_api_base.TestAPI):

  @classmethod
  def setUpClass(cls):
    tasks_api.app.config.from_object(InMemoryTestConfig)
    tasks_api.connect_db()

  @classmethod
  def tearDownClass(cls):
    tasks_api.disconnect_db()

  def setUp(self):
    self.app = tasks_api.app.test_client()
    tasks_api.clear_db()

  def tearDown(self):
    tasks_api.clear_db()