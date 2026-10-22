
WITH matches AS (
    SELECT season, matchweek
    FROM {{ ref('stg_matches') }}
),

performance AS (
    SELECT season, matchweek
    FROM {{ ref('fct_match_performance') }}
),

missing_matches AS (
    SELECT season, matchweek FROM matches
    EXCEPT ALL
    SELECT season, matchweek FROM performance
),

unexpected_matches AS (
    SELECT season, matchweek FROM performance
    EXCEPT ALL
    SELECT season, matchweek FROM matches
)

SELECT * FROM missing_matches
UNION ALL
SELECT * FROM unexpected_matches
