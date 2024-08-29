POSTGRES_USER = 'postgres_user'
POSTGRES_PASSWORD = 'postgres_password'
POSTGRES_DATABASE = 'postgres_database'
CONNECTION_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres-market-data-btcusd:5432/{POSTGRES_DATABASE}"
BTCUSD_FOLDER_PATH = r'dataset/*.csv'
SCHEMA_NAME = 'market_data'
TABLE_NAME = 'btcusd'
