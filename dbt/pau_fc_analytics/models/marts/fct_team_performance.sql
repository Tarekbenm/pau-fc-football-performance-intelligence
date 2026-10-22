
SELECT
    season,

    COUNT(*) AS matches_played,

    SUM(CASE WHEN result = 'W' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN result = 'D' THEN 1 ELSE 0 END) AS draws,
    SUM(CASE WHEN result = 'L' THEN 1 ELSE 0 END) AS losses,

    SUM(points) AS total_points,

    ROUND(AVG(points)::numeric, 2) AS points_per_match,

    SUM(goals_for) AS goals_scored,
    SUM(goals_against) AS goals_conceded,
    SUM(goal_difference) AS goal_difference,

    ROUND(AVG(possession)::numeric, 2) AS avg_possession

FROM {{ ref('stg_matches') }}

GROUP BY season
