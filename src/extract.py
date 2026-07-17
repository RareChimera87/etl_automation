import requests, logging
from tenacity import retry, stop_after_attempt, wait_fixed

logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
def fetch_data(url, params):
    logging.info("Starting the data extraction process...")
    try:

        response = requests.get(url, params=params, timeout=10)

        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()

        return data

    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred, retrying: {conn_err}")
        raise
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            logging.error(f"Resource not found, not retrying: {http_err}")
            return None
        logging.error(f"HTTP error occurred, retrying: {http_err}")
        raise  # Re-raise the exception to trigger retry
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Request timed out, retrying: {timeout_err}")
        raise

    except Exception as err:
        logging.error(f"An error occurred: {err}")
        raise
