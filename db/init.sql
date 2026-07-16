CREATE SCHEMA IF NOT EXISTS etl_automation_project;

CREATE TABLE IF NOT EXISTS etl_automation_project.crypto_prices (
    coin_id VARCHAR(70) NOT NULL,
    coin_symbol VARCHAR(10) NOT NULL,
    coin_name VARCHAR(255) NOT NULL,
    current_price_usd NUMERIC(20, 10) NOT NULL,
    market_cap_usd NUMERIC(20, 2) NOT NULL,
    total_volume_usd NUMERIC(20, 2) NOT NULL,
    high_24h_usd NUMERIC(20, 10) NOT NULL,
    low_24h_usd NUMERIC(20, 10) NOT NULL,
    price_change_pct_24h NUMERIC(10, 5) NOT NULL,
    last_updated_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    extracted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

    PRIMARY KEY (coin_id, extracted_at)
);