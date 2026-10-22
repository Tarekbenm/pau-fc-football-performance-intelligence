
SELECT
    season,
    matchweek,
    COUNT(*) AS match_count

FROM {{ ref('stg_matches') }}

GROUP BY season, matchweek

HAVING COUNT(*) > 1
