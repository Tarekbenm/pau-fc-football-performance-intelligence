
SELECT
    season,
    matchweek,
    shots_for,
    shots_against,
    shots_on_target_for,
    shots_on_target_against,
    penalty_goals_for,
    penalty_goals_against,
    penalty_attempts_for,
    penalty_attempts_against

FROM {{ source('pau_fc', 'shooting') }}
