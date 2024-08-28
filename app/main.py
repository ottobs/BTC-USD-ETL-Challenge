import logging
import pandas as pd
import time
from config import CONNECTION_URL, BTCUSD_FOLDER_PATH, SCHEMA_NAME, TABLE_NAME
from data_processing.data_reader import read_btcusd_data
from data_processing.datetime_handler import create_datetime_column
from data_processing.dataframe_transform import filter_dataframe, convert_dataframe_columns
from database.db_operations import get_latest_datetime_in_table, send_data

'''
This project ingests BTC trading data to the PostgeSQL table `market_data`.`btcusd`
'''

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the BTC-USD ETL process.")
    # This reads from the existing table in PostgreSQL and fetches the latest timestamp available
    # Our objective is to ingest only what is new, in order to avoid duplicates
    latest_datetime_in_table = get_latest_datetime_in_table(CONNECTION_URL)

    # We read the data from the .csv files, and perform the necessary checks and transformations
    df_btcusd = read_btcusd_data(BTCUSD_FOLDER_PATH)
    df_btcusd_with_date_time_column = create_datetime_column(df_btcusd)
    df_btcusd_new_data_only = filter_dataframe(df_btcusd_with_date_time_column, latest_datetime_in_table)
    df_btcusd_final = convert_dataframe_columns(df_btcusd_new_data_only)

    # It was agreed that we can omit rows with only null values. `drop_nulls()` is used to achieve this.
    # Also, we convert the polars dataframe to pandas, so we can leverage pandas.DataFrame.to_sql
    # when sending our data to our PostgreSQL table market_data.btcusd 
    df_pandas = df_btcusd_final.drop_nulls().collect().to_pandas()


    send_data(connection_url=CONNECTION_URL, schema_name=SCHEMA_NAME, table_name=TABLE_NAME, df=df_pandas)
    print(f"Data sample: {df_pandas.tail()}")
    logger.info("ETL process completed successfully.\n")

if __name__ == "__main__":
    # The code waits for PostgreSQL to be ready
    time.sleep(60)
    main()
