from datetime import datetime, timezone
import pandas as pd

def transform_data(data):
    """
    Transforms the raw data into a structured format.

    Args:
        data (list): Raw data fetched from the API.

    Returns:
        pd.DataFrame: Transformed data in a pandas DataFrame.
    """
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(data)

    # Select relevant columns (you can adjust this based on your needs)
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

    # Rename columns for clarity
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
    return df