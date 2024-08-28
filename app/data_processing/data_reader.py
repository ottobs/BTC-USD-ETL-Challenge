import polars as pl
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def read_btcusd_data(folder_path):
    logger.info(f"Reading BTC-USD data from {folder_path}")
    df = pl.scan_csv(folder_path, include_file_paths='path')

    # Validate the DataFrame
    if not validate_dataframe(df):
        raise ValueError("DataFrame validation failed. Please check the input data.")
    logger.info(f"Successfully initiated reading BTC-USD data.")
    return df

def validate_dataframe(df):
    expected_schema = {
        "Time": pl.Utf8,
        "Open": pl.Utf8,
        "High": pl.Utf8,
        "Low": pl.Utf8,
        "Close": pl.Utf8,
        "Volume_(BTC)": pl.Utf8,
        "Volume_(Currency)": pl.Utf8,
        "Weighted_Price": pl.Utf8,
        "path": pl.Utf8
    }

    actual_schema = df.collect().schema  # Collect the LazyFrame to resolve schema

    for col, expected_type in expected_schema.items():
        if col not in actual_schema:
            raise ValueError(f"Missing expected column: {col}")
        actual_type = actual_schema[col]
        if actual_type != expected_type:
            raise TypeError(f"Column {col} expected type {expected_type} but got {actual_type}")
    
    logging.info("DataFrame passed all validation checks.")
    return True