
-- ==================================
-- Create Clean Schema
-- ==================================

CREATE SCHEMA IF NOT EXISTS clean;

-- ==================================
-- Dimension: Season
-- ==================================

CREATE TABLE IF NOT EXISTS clean.dim_season (
    season_id SMALLINT PRIMARY KEY,
    CONSTRAINT valid_season
        CHECK (season_id BETWEEN 1 AND 4)
);

-- ==================================
-- Dimension: Weather
-- ==================================

CREATE TABLE IF NOT EXISTS clean.dim_weather (
    weather_id SMALLINT PRIMARY KEY,
    CONSTRAINT valid_weather
        CHECK (weather_id BETWEEN 1 AND 4)
);

-- ==================================
-- Dimension: Date
-- ==================================

CREATE TABLE IF NOT EXISTS clean.dim_date (
    dteday DATE PRIMARY KEY,
    yr SMALLINT NOT NULL CHECK (yr BETWEEN 0 AND 1),
    mnth SMALLINT NOT NULL CHECK (mnth BETWEEN 1 AND 12),
    weekday SMALLINT NOT NULL CHECK (weekday BETWEEN 0 AND 6),
    holiday SMALLINT NOT NULL CHECK (holiday BETWEEN 0 AND 1),
    workingday SMALLINT NOT NULL CHECK (workingday BETWEEN 0 AND 1)
);

-- ==================================
-- Fact Table: Hourly Bike Sharing
-- ==================================

CREATE TABLE IF NOT EXISTS clean.fact_hour (
    instant BIGINT PRIMARY KEY,

    dteday DATE NOT NULL,
    season_id SMALLINT NOT NULL,
    weather_id SMALLINT NOT NULL,

    hr SMALLINT NOT NULL CHECK (hr BETWEEN 0 AND 23),

    temp DOUBLE PRECISION NOT NULL CHECK (temp BETWEEN 0 AND 1),
    atemp DOUBLE PRECISION NOT NULL CHECK (atemp BETWEEN 0 AND 1),
    hum DOUBLE PRECISION NOT NULL CHECK (hum BETWEEN 0 AND 1),
    windspeed DOUBLE PRECISION NOT NULL CHECK (windspeed BETWEEN 0 AND 1),

    casual INTEGER NOT NULL CHECK (casual >= 0),
    registered INTEGER NOT NULL CHECK (registered >= 0),
    cnt INTEGER NOT NULL CHECK (cnt >= 0),

    CONSTRAINT fk_date
        FOREIGN KEY (dteday)
        REFERENCES clean.dim_date(dteday),

    CONSTRAINT fk_season
        FOREIGN KEY (season_id)
        REFERENCES clean.dim_season(season_id),

    CONSTRAINT fk_weather
        FOREIGN KEY (weather_id)
        REFERENCES clean.dim_weather(weather_id),

    CONSTRAINT valid_total_count
        CHECK (cnt = casual + registered)
);
