
import logging
from pathlib import Path

import pandas as pd


# ==================================
# Paths and Configuration
# ==================================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "hour.csv"
CLEAN_DATA_PATH = BASE_DIR / "data" / "processed" / "hour_clean.csv"

REQUIRED_COLUMNS = [
    "instant", "dteday", "season", "yr", "mnth", "hr",
    "holiday", "weekday", "workingday", "weathersit",
    "temp", "atemp", "hum", "windspeed",
    "casual", "registered", "cnt"
]


# ==================================
# Logging Configuration
# ==================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ==================================
# Data Cleaning Function
# ==================================

def clean_data():

    logger.info("Starting data cleaning process")

    # 1. Check source file
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw data file not found: {RAW_DATA_PATH}"
        )

    # 2. Load raw data
    df = pd.read_csv(RAW_DATA_PATH)

    raw_count = len(df)

    logger.info("Raw records: %d", raw_count)

    # 3. Check required columns
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Keep only the expected columns
    df = df[REQUIRED_COLUMNS].copy()

    # 4. Convert data types
    numeric_columns = [
        "instant", "season", "yr", "mnth", "hr",
        "holiday", "weekday", "workingday", "weathersit",
        "temp", "atemp", "hum", "windspeed",
        "casual", "registered", "cnt"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["dteday"] = pd.to_datetime(
        df["dteday"],
        errors="coerce"
    )

    # 5. Handle missing values
    before_missing = len(df)

    df = df.dropna(subset=REQUIRED_COLUMNS)

    logger.info(
        "Rows removed due to missing/invalid types: %d",
        before_missing - len(df)
    )

    # 6. Remove duplicate rows
    before_duplicates = len(df)

    df = df.drop_duplicates()

    logger.info(
        "Duplicate rows removed: %d",
        before_duplicates - len(df)
    )

    # 7. Validate business rules
    valid = (
        df["instant"].gt(0)
        & df["season"].between(1, 4)
        & df["yr"].between(0, 1)
        & df["mnth"].between(1, 12)
        & df["hr"].between(0, 23)
        & df["holiday"].between(0, 1)
        & df["weekday"].between(0, 6)
        & df["workingday"].between(0, 1)
        & df["weathersit"].between(1, 4)
        & df["temp"].between(0, 1)
        & df["atemp"].between(0, 1)
        & df["hum"].between(0, 1)
        & df["windspeed"].between(0, 1)
        & df["casual"].ge(0)
        & df["registered"].ge(0)
        & df["cnt"].ge(0)
        & (df["cnt"] == df["casual"] + df["registered"])
    )

    before_validation = len(df)

    df = df[valid].copy()

    logger.info(
        "Invalid rows removed: %d",
        before_validation - len(df)
    )

    # 8. Remove duplicate primary-key values
    before_ids = len(df)

    df = df.drop_duplicates(subset=["instant"], keep="first")

    logger.info(
        "Duplicate IDs removed: %d",
        before_ids - len(df)
    )

    # 9. Enforce integer data types
    integer_columns = [
        "instant", "season", "yr", "mnth", "hr",
        "holiday", "weekday", "workingday", "weathersit",
        "casual", "registered", "cnt"
    ]

    for col in integer_columns:
        df[col] = df[col].astype("int64")

    # 10. Final validation
    if df.empty:
        raise ValueError("Cleaning produced an empty dataset")

    if df["instant"].duplicated().any():
        raise ValueError("Duplicate primary keys found after cleaning")

    if df[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError("Null values found after cleaning")

    clean_count = len(df)

    # 11. Save clean data separately
    CLEAN_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(CLEAN_DATA_PATH, index=False)

    # 12. Cleaning summary
    logger.info("Cleaning completed successfully")
    logger.info("Raw row count: %d", raw_count)
    logger.info("Clean row count: %d", clean_count)
    logger.info("Removed rows: %d", raw_count - clean_count)
    logger.info("Clean file saved at: %s", CLEAN_DATA_PATH)


if __name__ == "__main__":
    clean_data()
