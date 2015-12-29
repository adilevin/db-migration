import in_memory_dao
import migration_dao
import mongodb_dao
import sqlite_dao

def create_mongodb_dao(config):
    return mongodb_dao.Mongo(
        connection_uri=config['mongodb_connection_uri'],
        database_name=config['mongodb_database_name'])

def create_sqlite_dao(config):
    return sqlite_dao.SQLiteRepo(config['sqlite_file_path'])

def create_dao(config):
    if config['repository'] == 'migrate_from_sqlite_to_mongodb':
        return migration_dao.MigrationDAO(
            create_sqlite_dao(config),
            create_mongodb_dao(config),
            config['migration_step'])
    elif config['repository'] == 'mongodb':
        return create_mongodb_dao(config)
    elif config['repository'] == 'inmemory':
        return in_memory_dao.InMemoryRepo()
    elif config['repository'] == 'sqlite':
        return create_sqlite_dao(config)
    else:
        raise 'Invalid "repository" configuration attribute'