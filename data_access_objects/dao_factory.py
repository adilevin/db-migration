import in_memory_dao
import migration_dao
from mongodb_dao import MongoDBDAO
from sqlite_dao import SQLiteDAO

def create_dao(config):
    if config['repository'] == 'migrate_from_sqlite_to_mongodb':
        return migration_dao.MigrationDAO(
            SQLiteDAO(config),
            MongoDBDAO(config),
            config['migration_step'])
    elif config['repository'] == 'mongodb':
        return MongoDBDAO(config)
    elif config['repository'] == 'inmemory':
        return in_memory_dao.InMemoryRepo()
    elif config['repository'] == 'sqlite':
        return SQLiteDAO(config)
    else:
        raise 'Invalid "repository" configuration attribute'