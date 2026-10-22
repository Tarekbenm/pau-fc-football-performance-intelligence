SELECT
    season,
    player_id,
    COUNT(*) AS row_count

FROM {{ ref('fct_player_performance') }}

GROUP BY
    season,
    player_id

HAVING COUNT(*) > 1
