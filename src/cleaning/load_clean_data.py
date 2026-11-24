
import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, URL
from dotenv import load_dotenv
import os


# ==================================
# Paths and Configuration
# ==================================

BASE_DIR = Path(__file__).resolve().parents[2]

CLEAN_DATA_PATH = BASE_DIR / "data" / "processed" / "hour_clean.csv"

load_dotenv(BASE_DIR / ".env")


# ==================================
# Logging Configuration
# ==================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ==================================
# Database Connection
# ==================================

def get_engine():

    required_vars = [
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME"
    ]

    missing = [
        var for var in required_vars
        if not os.getenv(var)
    ]

    if missing:
        raise ValueError(
            f"Missing environment variables: {missing}"
        )

    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
    )

    return create_engine(db_url)


# ==================================
# Load Clean Data
# ==================================

def load_clean_data():

    logger.info("Starting clean data loading")

    if not CLEAN_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Clean data file not found: {CLEAN_DATA_PATH}"
        )

    df = pd.read_csv(CLEAN_DATA_PATH)

    logger.info("Clean records found: %d", len(df))

    # Convert date column
    df["dteday"] = pd.to_datetime(
        df["dteday"]
    ).dt.date

    engine = get_engine()

    try:
        with engine.begin() as connection:

            # 1. Load Season Dimension
            seasons = pd.DataFrame({
                "season_id": sorted(df["season"].unique())
            })

            seasons.to_sql(
                "dim_season",
                con=connection,
                schema="clean",
                if_exists="append",
                index=False
            )

            logger.info("Season dimension loaded")

            # 2. Load Weather Dimension
            weather = pd.DataFrame({
                "weather_id": sorted(df["weathersit"].unique())
            })

            weather.to_sql(
                "dim_weather",
                con=connection,
                schema="clean",
                if_exists="append",
                index=False
            )

            logger.info("Weather dimension loaded")

            # 3. Load Date Dimension
            dates = df[
                [
                    "dteday",
                    "yr",
                    "mnth",
                    "weekday",
                    "holiday",
                    "workingday"
                ]
            ].drop_duplicates(subset=["dteday"])

            dates.to_sql(
                "dim_date",
                con=connection,
                schema="clean",
                if_exists="append",
                index=False
            )

            logger.info("Date dimension loaded")

            # 4. Prepare Fact Table
            fact = df.rename(
                columns={
                    "season": "season_id",
                    "weathersit": "weather_id"
                }
            )

            fact = fact[
                [
                    "instant",
                    "dteday",
                    "season_id",
                    "weather_id",
                    "hr",
                    "temp",
                    "atemp",
                    "hum",
                    "windspeed",
                    "casual",
                    "registered",
                    "cnt"
                ]
            ]

            fact.to_sql(
                "fact_hour",
                con=connection,
                schema="clean",
                if_exists="append",
                index=False
            )

            logger.info("Fact table loaded")

        logger.info("All clean data loaded successfully")

    except Exception:
        logger.exception("Clean data loading failed")
        raise

    finally:
        engine.dispose()


if __name__ == "__main__":
    load_clean_data()
