import os, logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table
from tenacity import retry, stop_after_attempt, wait_fixed
from sqlalchemy.dialects.postgresql import insert


logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

load_dotenv()
ENV = os.getenv("ENV")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


@retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
def create_db_engine():
    logging.info("Creating database engine...")
    try:
        db = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        if ENV == "production":
            engine = create_engine(db, echo=False)
        else:
            engine = create_engine(db, echo=True)

        return engine

    except Exception as e:
        logging.error(f"Error creating database engine: {e}")
        raise

        
        
engine = create_db_engine()
metadata = MetaData()
crypto_prices_table = Table("crypto_prices", metadata, autoload_with=engine)


@retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
def load_data(df):
    data = df.to_dict(orient="records")
    logging.info("Starting the data loading process...")
    stmt = insert(crypto_prices_table).values(data)
    stmt = stmt.on_conflict_do_update(
        index_elements=["coin_id" , "extracted_at"],  
        set_={i: stmt.excluded[i] for i in df.columns if i not in ["coin_id", "extracted_at"]}
        )
    with engine .connect() as conn:
        try:
            conn.execute(stmt)
            conn.commit()
            logging.info("Data loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise