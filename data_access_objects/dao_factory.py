
def create_dao(config):
    if config['repository'] == 'migrate_from_sqlite_to_mongodb':
        import sqlite_to_mongo_migration_dao
        return sqlite_to_mongo_migration_dao.MigrationDAO(config)
    elif config['repository'] == 'mongodb':
        import mongodb_dao
        return mongodb_dao.Mongo(
            connection_uri=config['mongodb_connection_uri'],
            database_name=config['mongodb_database_name'])
    elif config['repository'] == 'inmemory':
        import in_memory_dao
        return in_memory_dao.InMemoryRepo()
    elif config['repository'] == 'sqlite':
        import sqlite_dao
        return sqlite_dao.SQLiteRepo(config['sqlite_file_path'])
    else:
        raise 'Invalid "repository" configuration attribute'