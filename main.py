import tasks_api
tasks_api.app.config.from_pyfile('test_config.py')
tasks_api.connect_db()
tasks_api.app.run()

