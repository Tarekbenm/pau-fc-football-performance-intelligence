SELECT
    season,
    player_id,
    player_name,
    goals,
    assists,
    goal_contributions

FROM {{ ref('fct_player_performance') }}

WHERE
    goals IS NULL
    OR assists IS NULL
    OR goal_contributions IS NULL
    OR goals + assists <> goal_contributions
