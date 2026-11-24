# Bike Sharing Data Engineering Project

## 1. Project Overview

This project implements a data engineering pipeline using the Bike Sharing Dataset. The main objective is to clean, validate, store, and analyze bike rental data using Python, Docker, PostgreSQL, and SQL.

The project transforms raw bike-sharing data into a structured relational database and performs data quality checks to ensure data reliability.

## 2. Dataset Description

The project uses the Bike Sharing Dataset (`hour.csv`).

- **Records:** 17,379 hourly records
- **Features:** 17 columns
- **Data granularity:** Hourly bike rental records
- **Target variable:** `cnt` (total bike rentals)

The dataset contains information about dates, seasons, weather conditions, temperature, humidity, wind speed, and rental counts.

## 3. Technologies Used

- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- Docker and Docker Compose
- SQL
- Jupyter Notebook

## 4. Project Structure

```text
bike-sharing-project/
│
├── data/
│   ├── raw/
│   │   └── hour.csv
│   └── processed/
│       └── hour_clean.csv
│
├── doc/
│   ├── data_dictionary.md
│   ├── phase2_results.md
│   └── project_proposal.md
│
├── notebook/
│   └── 01_data_exploration.ipynb
│
├── sql/
│   ├── clean_schema.sql
│   ├── analytical.query.sql
│   └── intentional_bad_data_test.sql
│
├── src/
│   ├── ingestion/
│   │   └── ingest_data.py
│   ├── cleaning/
│   │   ├── clean_data.py
│   │   └── load_clean_data.py
│   ├── quality/
│   │   └── quality_checks.py
│   └── analytics/
│       └── analysis.py
│
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## 5. Data Pipeline

The project pipeline consists of the following stages:

1. **Data Ingestion:** Load the raw Bike Sharing dataset.
2. **Data Cleaning:** Validate columns, handle missing or invalid values, remove duplicates, and apply business rules.
3. **Database Design:** Create a relational schema in PostgreSQL containing dimension and fact tables.
4. **Data Loading:** Load the cleaned data into PostgreSQL.
5. **Data Analysis:** Use SQL queries and analytical views to explore bike rental demand.
6. **Data Quality:** Execute automated checks to validate the loaded data.

## 6. Database Design

The PostgreSQL database uses a relational structure under the `clean` schema.

Main tables:

- `dim_season`
- `dim_weather`
- `dim_date`
- `fact_hour`

The fact table stores hourly rental measurements and references the dimension tables through foreign keys.

## 7. Data Quality Checks

The automated quality pipeline validates:

- Primary key uniqueness
- Foreign key integrity
- NULL values
- Numeric ranges and business rules
- Raw versus cleaned row counts

The pipeline uses PASS/FAIL results and stops execution when a quality check fails.

The project also includes an intentional bad-data test to verify that invalid records can be detected.

## 8. How to Run the Project

### Prerequisites

- Python 3
- Docker Desktop
- PostgreSQL through Docker Compose

### Step 1: Clone the repository

```bash
git clone <repository-url>
cd <project-folder>
```

### Step 2: Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a local `.env` file based on `.env.example` and configure the database credentials.

Do not upload `.env` to GitHub.

### Step 5: Start PostgreSQL and pgAdmin

```bash
docker compose up -d pgdatabase pgadmin
```

### Step 6: Run data cleaning

```bash
python src/cleaning/clean_data.py
```

### Step 7: Create the database schema

Execute:

```text
sql/clean_schema.sql
```

against the project PostgreSQL database.

### Step 8: Load cleaned data

```bash
python src/cleaning/load_clean_data.py
```

### Step 9: Run data quality checks

```bash
python src/quality/quality_checks.py
```

### Step 10: Run SQL analysis

Execute the queries in:

```text
sql/analytical.query.sql
```

## 9. Data Quality Results

The final automated data quality execution completed successfully.

All implemented checks returned PASS:

- Primary Key Uniqueness
- Foreign Key Integrity
- NULL Values
- Numeric Ranges and Business Rules
- Raw vs Clean Row Count

The raw and cleaned datasets contain 17,379 records each.

## 10. Project Deliverables

- Raw and cleaned datasets
- Python data cleaning and loading scripts
- PostgreSQL relational schema
- SQL analytical queries and views
- Automated data quality checks
- Intentional bad-data testing script
- Project documentation

## 11. Security Notes

Database credentials are stored in a local `.env` file. The `.env` file must not be committed to version control. Use `.env.example` to document the required environment variable names without exposing passwords.