from datetime import datetime, timezone
import pandas as pd
import logging

logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def transform_data(data):
    logging.info("Starting the data transformation process...")
    """
    Transforms the raw data into a structured format.

    Args:
        data (list): Raw data fetched from the API.

    Returns:
        pd.DataFrame: Transformed data in a pandas DataFrame.
    """
    
    df = pd.DataFrame(data)

    
    relevant_columns = [
        "id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
        "total_volume",
        "high_24h",
        "low_24h",
        "price_change_percentage_24h",
        "last_updated"
    ]
    df = df[relevant_columns]

    logging.info("Relevant columns selected.")
    df.rename(columns={
        "id": "coin_id",
        "symbol": "coin_symbol",
        "name": "coin_name",
        "current_price": "current_price_usd",
        "market_cap": "market_cap_usd",
        "total_volume": "total_volume_usd",
        "high_24h": "high_24h_usd",
        "low_24h": "low_24h_usd",
        "price_change_percentage_24h": "price_change_pct_24h",
        "last_updated": "last_updated_timestamp",

    }, inplace=True)
    df["last_updated_timestamp"] = pd.to_datetime(df["last_updated_timestamp"])
    df["extracted_at"] = datetime.now(timezone.utc) 
    logging.info("Data transformation completed successfully.")
    return df