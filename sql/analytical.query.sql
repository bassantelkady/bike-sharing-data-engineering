SELECT
    season,
    AVG(cnt) AS avg_rentals
FROM bike_sharing
GROUP BY season;