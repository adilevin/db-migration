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
            'sqlite_file_path' : 'sqlite_prod.db',
        }

tasks_api.app.config.from_object(ProductionConfig)
tasks_api.connect_db()
tasks_api.app.run()

