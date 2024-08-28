import polars as pl
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def filter_dataframe(df, latest_timestamp):
    if latest_timestamp:
        try:
            logger.info(f"Filtering DataFrame for entries after {latest_timestamp}")
            df = df.filter(pl.col("date_time") > pl.lit(latest_timestamp))
            return df
        except Exception as e:
            logger.error(f"There was a probme when filtering the dataframe by timestamp: {e}")
            raise
    logger.info(f"Latest timestamp is not available. Returning the whole dataframe")
    return df

def convert_dataframe_columns(df):
    try:
        df = df.with_columns([
            pl.col("Open").cast(pl.Float64).alias("open_price"),
            pl.col("High").cast(pl.Float64).alias("high_price"),
            pl.col("Low").cast(pl.Float64).alias("low_price"),
            pl.col("Close").cast(pl.Float64).alias("close_price"),
            pl.col("Volume_(BTC)").cast(pl.Float64).alias("volume_btc"),
            pl.col("Volume_(Currency)").cast(pl.Float64).alias("volume_usd"),  
            pl.col("Weighted_Price").cast(pl.Float64).alias("weighted_price")
        ])

        df = df.drop([
            "Open", "High", "Low", "Close",
            "Volume_(BTC)", "Volume_(Currency)",
            "Weighted_Price", "Time", "date",
            "datetime_str", "path"
        ])

        return df
    except Exception as e:
        logger.error(f"An error occurred while converting the dataframe column: {e}")
        raise