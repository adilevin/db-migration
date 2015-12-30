import tasks_api
import json
import sys
try:
    port = int(sys.argv[1])
except:
    port = 8000

appConfig = {
    'mongodb_connection_uri' : 'mongodb://localhost:27017/',
    'mongodb_database_name' : 'prod',
    'sqlite_file_path' : 'c:/sqlite/sqlite_prod.db',
    'port' : port
}

appConfig['repository'] = 'mongodb' # 'mongodb', 'sqlite', 'migrate_from_sqlite_to_mongodb', 'inmemory'

class ProductionConfig(object):
    ENVIRONMENT = appConfig
tasks_api.app.config.from_object(ProductionConfig)
print json.dumps(tasks_api.app.config['ENVIRONMENT'],indent=True)

print 'Connecting to database...'
tasks_api.connect_db()
print 'Database is connected'
from gevent.wsgi import WSGIServer
http_server = WSGIServer(('', port), tasks_api.app)
http_server.serve_forever()

# tasks_api.app.run() - this is the Flask default server, which is must less efficient

