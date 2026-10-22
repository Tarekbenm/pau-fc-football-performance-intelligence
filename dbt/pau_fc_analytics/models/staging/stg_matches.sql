
{{ config(materialized='view') }}

SELECT
    match_date,
    season,
    matchweek,
    opponent,
    venue,
    result,
    goals_for,
    goals_against,
    goal_difference,
    possession,
    formation,
    opponent_formation,
    points
FROM {{ source('pau_fc', 'matches') }}
