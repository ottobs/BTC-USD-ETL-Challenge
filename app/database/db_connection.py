from sqlalchemy import create_engine

def get_database_engine(connection_url):
    return create_engine(connection_url)
