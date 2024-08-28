CREATE SCHEMA IF NOT EXISTS market_data;

CREATE TABLE IF NOT EXISTS market_data.btcusd (
    date_time TIMESTAMP,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT,
    volume_btc FLOAT,
    volume_usd FLOAT,
    weighted_price FLOAT
);