import os
import pandas as pd
from sqlalchemy import create_engine, URL
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

# Database connection
db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(db_url)

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# CSV file path
DATA_PATH = BASE_DIR / "data" / "raw" / "hour.csv"

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg2://bike_user:YOUR_PASSWORD@localhost:5432/bike_sharing"
)

def ingest_data():
    print("Reading CSV file...")

    df = pd.read_csv(DATA_PATH, parse_dates=["dteday"])

    print(f"Rows loaded from CSV: {len(df)}")

    print("Connecting to PostgreSQL...")

    df.to_sql(
        name="hour",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Data successfully loaded into PostgreSQL!")

    print(f"Total records inserted: {len(df)}")


if __name__ == "__main__":
    ingest_data()
