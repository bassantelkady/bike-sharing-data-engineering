
-- ==========================================
-- Analysis 1: Bike Demand by Season & Weather
-- ==========================================

SELECT
    s.season_id,
    CASE s.season_id
        WHEN 1 THEN 'Spring'
        WHEN 2 THEN 'Summer'
        WHEN 3 THEN 'Fall'
        WHEN 4 THEN 'Winter'
    END AS season_name,

    w.weather_id,
    f.cnt AS hourly_rentals,

    ROUND(AVG(f.cnt) OVER (
        PARTITION BY s.season_id, w.weather_id
    ), 2) AS avg_hourly_rentals,

    SUM(f.cnt) OVER (
        PARTITION BY s.season_id, w.weather_id
    ) AS total_rentals

FROM clean.fact_hour f

JOIN clean.dim_season s
    ON f.season_id = s.season_id

JOIN clean.dim_weather w
    ON f.weather_id = w.weather_id

ORDER BY
    s.season_id,
    w.weather_id,
    f.instant;



-- ==========================================
-- Analytical View 1:
-- Bike Demand by Season and Weather
-- ==========================================

CREATE OR REPLACE VIEW clean.vw_demand_by_season_weather AS

SELECT
    s.season_id,

    CASE s.season_id
        WHEN 1 THEN 'Spring'
        WHEN 2 THEN 'Summer'
        WHEN 3 THEN 'Fall'
        WHEN 4 THEN 'Winter'
    END AS season_name,

    w.weather_id,

    CASE w.weather_id
        WHEN 1 THEN 'Clear'
        WHEN 2 THEN 'Mist and Cloudy'
        WHEN 3 THEN 'Light Rain or Snow'
        WHEN 4 THEN 'Heavy Rain or Snow'
    END AS weather_condition,

    COUNT(*) AS total_hours,

    SUM(f.cnt) AS total_rentals,

    ROUND(AVG(f.cnt), 2) AS avg_hourly_rentals

FROM clean.fact_hour f

JOIN clean.dim_season s
    ON f.season_id = s.season_id

JOIN clean.dim_weather w
    ON f.weather_id = w.weather_id

GROUP BY
    s.season_id,
    w.weather_id

ORDER BY
    s.season_id,
    w.weather_id;



-- ==========================================
-- Analytical View 2:
-- Bike Demand by Hour and Day Type
-- ==========================================

CREATE OR REPLACE VIEW clean.vw_demand_by_hour_and_day_type AS

SELECT
    f.hr,

    CASE
        WHEN d.workingday = 1 THEN 'Working Day'
        ELSE 'Non-Working Day'
    END AS day_type,

    COUNT(*) AS total_hours,

    SUM(f.cnt) AS total_rentals,

    ROUND(AVG(f.cnt), 2) AS avg_hourly_rentals

FROM clean.fact_hour f

JOIN clean.dim_date d
    ON f.dteday = d.dteday

GROUP BY
    f.hr,
    d.workingday;
