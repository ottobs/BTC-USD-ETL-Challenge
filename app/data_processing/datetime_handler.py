import polars as pl
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_datetime_column(df):
    try:
        logger.info("Creating datetime column from 'date' and 'Time' columns.")
        df = df.with_columns(
            pl.col("path").str.extract(r"(\d{4}-\d{2}-\d{2})", 1).alias("date")
        )

        df = df.with_columns(
            (pl.col("date") + " " + pl.col("Time")).alias("datetime_str")
        )

        df = df.with_columns(
            pl.col("datetime_str").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False).alias("date_time")
        )
        logger.info("Datetime column created successfully.")
        return df
    except Exception as e:
        raise Exception(f"There was a problem when creating the date_time column. Error {e}")