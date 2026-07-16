import os, schedule, time, extract, logging, transform
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV")

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd"
}

logging.basicConfig(
    filename="extract.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def run(): 
    logging.info("Starting etl process...")
    try:
        data = extract.fetch_data(url, params)
        if data is None:

            raise ValueError("No data fetched. Skipping transformation.")
        logging.info("Data fetched successfully.")
        transformed_data = transform.transform_data(data)
        print(transformed_data.head())  # Display the first few rows of the transformed data
        logging.info("Data transformed successfully.")

        #logging.info(f"Data: {data}")

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return
    except Exception as e:
        logging.error(f"An error occurred during the ETL process: {e}")
        return





if ENV == "production":
    schedule.every().hour.do(run)
else:
    schedule.every(10).seconds.do(run)



while True:
    schedule.run_pending()
    time.sleep(1)