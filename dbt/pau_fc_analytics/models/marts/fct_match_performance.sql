
SELECT
    m.season,
    m.matchweek,
    m.match_date,
    m.opponent,
    m.venue,
    m.result,
    m.goals_for,
    m.goals_against,
    m.goal_difference,
    m.possession,
    m.formation,
    m.opponent_formation,
    m.points,

    -- Résultats du match
    CASE WHEN m.result = 'W' THEN 1 ELSE 0 END AS is_win,
    CASE WHEN m.result = 'D' THEN 1 ELSE 0 END AS is_draw,
    CASE WHEN m.result = 'L' THEN 1 ELSE 0 END AS is_loss,

    CASE
        WHEN m.goals_against = 0 THEN 1
        ELSE 0
    END AS clean_sheet,

    -- Points cumulés par saison
    SUM(m.points) OVER (
        PARTITION BY m.season
        ORDER BY m.matchweek
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_points,

    -- Statistiques de tirs
    s.shots_for,
    s.shots_against,
    s.shots_on_target_for,
    s.shots_on_target_against,

    -- Différentiels de tirs
    s.shots_for - s.shots_against AS shot_difference,

    s.shots_on_target_for - s.shots_on_target_against
        AS shots_on_target_difference,

    -- Précision des tirs (%)
    ROUND(
        100.0 * s.shots_on_target_for / NULLIF(s.shots_for, 0),
        2
    ) AS shot_accuracy_pct,

    -- Conversion des tirs en buts (%)
    ROUND(
        100.0 * m.goals_for / NULLIF(s.shots_for, 0),
        2
    ) AS goal_conversion_pct,

    -- Statistiques des gardiens du Pau FC
    g.gk_shots_faced,
    g.gk_goals_conceded,
    g.gk_saves,
    g.gk_save_pct,
    g.gk_clean_sheet,
    g.gk_penalties_faced,
    g.gk_penalties_conceded,
    g.gk_penalties_saved,

    -- Statistiques des gardiens adverses
    g.opponent_gk_shots_faced,
    g.opponent_gk_goals_conceded,
    g.opponent_gk_saves,
    g.opponent_gk_save_pct, 

    -- Statistiques diverses du Pau FC
    d.yellow_cards_for,
    d.red_cards_for,
    d.second_yellow_cards_for,
    d.fouls_committed_for,
    d.fouls_drawn_for,
    d.offsides_for,
    d.crosses_for,
    d.interceptions_for,
    d.tackles_won_for,
    d.own_goals_for,

    -- Statistiques diverses des adversaires
    d.yellow_cards_against,
    d.red_cards_against,
    d.second_yellow_cards_against,
    d.fouls_committed_against,
    d.fouls_drawn_against,
    d.offsides_against,
    d.crosses_against,
    d.interceptions_against,
    d.tackles_won_against,
    d.own_goals_against


FROM {{ ref('stg_matches') }} AS m

LEFT JOIN {{ ref('stg_shooting') }} AS s
    ON m.season = s.season
    AND m.matchweek = s.matchweek

LEFT JOIN {{ ref('stg_goalkeeping') }} AS g
    ON m.season = g.season
    AND m.matchweek = g.matchweek

LEFT JOIN {{ ref('stg_divers') }} AS d
    ON m.season = d.season
    AND m.matchweek = d.matchweek


