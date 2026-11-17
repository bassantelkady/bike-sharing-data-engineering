
import os
import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, URL
from dotenv import load_dotenv

# Project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - INGEST-AUDIT-ECU 26 - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# CSV source
DATA_PATH = BASE_DIR / "data" / "raw" / "hour.csv"


def get_engine():
    """Create PostgreSQL database connection."""

    required_vars = [
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME"
    ]

    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        raise ValueError(f"Missing environment variables: {missing}")

    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
    )

    return create_engine(db_url)


def ingest_data():

    logger.info("Starting Bike Sharing ingestion")

    try:
        # Check source file
        if not DATA_PATH.exists():
            raise FileNotFoundError(f"Source file not found: {DATA_PATH}")

        logger.info("Source file found: %s", DATA_PATH.name)

        # Read raw data without cleaning or transformations
        df = pd.read_csv(DATA_PATH)

        total_records = len(df)

        logger.info("Source status: SUCCESS")
        logger.info("Total records fetched: %d", total_records)

        # Connect to PostgreSQL
        engine = get_engine()

        logger.info("Connecting to PostgreSQL")

        # Store raw data
        df.to_sql(
            name="hour",
            con=engine,
            if_exists="replace",
            index=False,
            chunksize=1000
        )

        logger.info("Raw data successfully stored")
        logger.info("Total records inserted: %d", total_records)

        engine.dispose()

    except Exception:
        logger.exception("Ingestion failed")
        raise

    finally:
        logger.info("Ingestion execution finished")


if __name__ == "__main__":
    ingest_data()
