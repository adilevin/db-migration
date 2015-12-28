import tasks_api


#class ProductionConfig(object):
#    ENVIRONMENT = {
#        'repository' : 'mongodb',
#        'mongodb_connection_uri' : 'mongodb://localhost:27017/',
#        'mongodb_database_name' : 'prod'
#    }

class ProductionConfig(object):
    ENVIRONMENT = {
            'repository':'sqlite',
            'sqlite_file_path' : 'sqlite_files/sqlite_prod.db',
        }

tasks_api.app.config.from_object(ProductionConfig)
tasks_api.connect_db()

if __name__=='__main__':
    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('', 5000), tasks_api.app)
    http_server.serve_forever()
    #tasks_api.app.run()

