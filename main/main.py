import tasks_api
import sys
try:
    port = int(sys.argv[1])
except:
    port = 8000

#class ProductionConfig(object):
#    ENVIRONMENT = {
#        'repository' : 'mongodb',
#        'mongodb_connection_uri' : 'mongodb://localhost:27017/',
#        'mongodb_database_name' : 'prod',
#        'port' : port
#    }

class ProductionConfig(object):
    ENVIRONMENT = {
            'repository':'sqlite',
            'sqlite_file_path' : 'c:/sqlite/sqlite_prod.db',
            'port' : port
        }


tasks_api.app.config.from_object(ProductionConfig)

import json
print json.dumps(tasks_api.app.config['ENVIRONMENT'],indent=True)

print 'Connecting to database...'
tasks_api.connect_db()
print 'Database is connected'
from gevent.wsgi import WSGIServer
http_server = WSGIServer(('', port), tasks_api.app)
http_server.serve_forever()

# tasks_api.app.run() - this is the Flask default server, which is must less efficient

