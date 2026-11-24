
import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text


# ==================================
# Configuration
# ==================================

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - DATA-QUALITY - %(levelname)s - %(message)s"
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
# Data Quality Checks
# ==================================

def run_quality_checks(engine):

    checks = {

        "Primary Key Uniqueness": """
            SELECT COUNT(*) - COUNT(DISTINCT instant)
            FROM clean.fact_hour;
        """,

        "Foreign Key Integrity": """
            SELECT COUNT(*)
            FROM clean.fact_hour f
            LEFT JOIN clean.dim_date d
                ON f.dteday = d.dteday
            LEFT JOIN clean.dim_season s
                ON f.season_id = s.season_id
            LEFT JOIN clean.dim_weather w
                ON f.weather_id = w.weather_id
            WHERE d.dteday IS NULL
               OR s.season_id IS NULL
               OR w.weather_id IS NULL;
        """,

        "NULL Values": """
            SELECT COUNT(*)
            FROM clean.fact_hour
            WHERE instant IS NULL
               OR dteday IS NULL
               OR season_id IS NULL
               OR weather_id IS NULL
               OR hr IS NULL
               OR cnt IS NULL;
        """,

        "Numeric Ranges and Business Rules": """
            SELECT COUNT(*)
            FROM clean.fact_hour
            WHERE hr NOT BETWEEN 0 AND 23
               OR temp NOT BETWEEN 0 AND 1
               OR atemp NOT BETWEEN 0 AND 1
               OR hum NOT BETWEEN 0 AND 1
               OR windspeed NOT BETWEEN 0 AND 1
               OR casual < 0
               OR registered < 0
               OR cnt < 0
               OR cnt <> casual + registered;
        """,

        "Raw vs Clean Row Count": """
            SELECT ABS(
                (SELECT COUNT(*) FROM public.hour)
                -
                (SELECT COUNT(*) FROM clean.fact_hour)
            );
        """
    }

    failed_checks = []

    with engine.connect() as connection:

        for check_name, query in checks.items():

            result = connection.execute(text(query)).scalar()

            if result == 0:
                logger.info("%s: PASS", check_name)

            else:
                logger.error(
                    "%s: FAIL - Invalid records: %s",
                    check_name,
                    result
                )

                failed_checks.append(check_name)

    if failed_checks:
        raise RuntimeError(
            f"Data Quality Failed: {failed_checks}"
        )

    logger.info("All Data Quality Checks Passed Successfully!")



# ==================================
# Intentional Bad Data Test
# ==================================

def test_bad_data_detection(engine):

    query = """
        SELECT COUNT(*)
        FROM clean.quality_test
        WHERE hr NOT BETWEEN 0 AND 23
           OR cnt < 0;
    """

    with engine.connect() as connection:
        invalid_records = connection.execute(
            text(query)
        ).scalar()

    if invalid_records > 0:
        logger.error(
            "Intentional Bad Data Test: FAIL - "
            "Detected %s invalid records",
            invalid_records
        )
        return False

    logger.info("Intentional Bad Data Test: PASS")
    return True



# ==================================
# Main Execution
# ==================================

def main():

    logger.info("Starting Data Quality Checks")

    engine = None

    try:
        engine = get_engine()

        logger.info("Connecting to PostgreSQL")

        run_quality_checks(engine)

        

        logger.info("Data Quality Pipeline: SUCCESS")

    except Exception:
        logger.exception("Data Quality Pipeline: FAILED")
        raise
    except Exception:
        logger.exception("Data Quality Pipeline: FAILED")
        raise

    finally:
        if engine:
            engine.dispose()

        logger.info("Data Quality Execution Finished")


if __name__ == "__main__":
    main()