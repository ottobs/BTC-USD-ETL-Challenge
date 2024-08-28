import pandas as pd
from database.db_connection import get_database_engine
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_latest_datetime_in_table(connection_url):
    try:
        logger.info("Fetching the latest datetime from the database.")
        engine = get_database_engine(connection_url)
        query = "SELECT MAX(date_time) AS latest_timestamp FROM market_data.btcusd"
        df = pd.read_sql(query, engine)
        latest_timestamp = df['latest_timestamp'].iloc[0]
        return latest_timestamp
    except Exception as e:
        logger.error(f"An error occurred while feching the latest timestamp in market_data.btcusd: {e}")
        raise

def send_data(connection_url, schema_name, table_name, df):
    try:
        logger.info(f"Sending data to {schema_name}.{table_name} in PostgreSQL database.")
        engine = get_database_engine(connection_url)
        df.to_sql(name=table_name, con=engine, schema=schema_name, if_exists='append', index=False)
        logger.info("Data sent successfully.")
    except Exception as e:
        logger.error(f"There as a problem when sending the data to market_data.btcusd: {e}")
        raise