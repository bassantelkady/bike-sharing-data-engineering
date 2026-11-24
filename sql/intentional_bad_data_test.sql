
-- Intentional Bad Data Test
-- Purpose: Verify that invalid records can be detected.

CREATE TABLE IF NOT EXISTS clean.quality_test (
    instant INTEGER PRIMARY KEY,
    hr INTEGER,
    cnt INTEGER
);

TRUNCATE TABLE clean.quality_test;

INSERT INTO clean.quality_test (instant, hr, cnt)
VALUES
    (1, 10, 100),
    (2, 25, 150),
    (3, 8, -50);

-- Detect invalid records
SELECT *
FROM clean.quality_test
WHERE hr NOT BETWEEN 0 AND 23
   OR cnt < 0;

-- Expected result: 2 invalid records
SELECT COUNT(*) AS invalid_records
FROM clean.quality_test
WHERE hr NOT BETWEEN 0 AND 23
   OR cnt < 0;

-- Cleanup test table
DROP TABLE clean.quality_test;
