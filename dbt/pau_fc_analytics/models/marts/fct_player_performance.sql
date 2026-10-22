SELECT
    season,
    player_id,
    player_name,
    nationality,
    position,
    age,

    -- Temps de jeu
    matches_played,
    starts,
    minutes_played,
    nineties,

    -- Contributions offensives
    goals,
    assists,
    goal_contributions,
    non_penalty_goals,
    penalty_goals,
    penalty_attempts,

    -- Discipline
    yellow_cards,
    red_cards,

    -- Performances par 90 minutes
    goals_per90,
    assists_per90,
    goal_contributions_per90,
    non_penalty_goals_per90,
    non_penalty_contributions_per90,

    -- Indicateur pour comparer les joueurs réguliers
    CASE
        WHEN minutes_played >= 900 THEN 1
        ELSE 0
    END AS has_significant_playtime

FROM {{ ref('stg_players') }}
