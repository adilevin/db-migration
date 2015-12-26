
def create_dao(config):
    if config['repository'] == 'mongodb':
        import mongodb_dao
        return mongodb_dao.Mongo(
            connection_uri=config['mongodb_connection_uri'],
            database_name=config['mongodb_database_name'])
    elif config['repository'] == 'inmemory':
        import in_memory_dao
        return in_memory_dao.InMemoryRepo()

