
SELECT
    season,
    matchweek,

    -- Pau FC
    yellow_cards_for,
    red_cards_for,
    second_yellow_cards_for,
    fouls_committed_for,
    fouls_drawn_for,
    offsides_for,
    crosses_for,
    interceptions_for,
    tackles_won_for,
    own_goals_for,

    -- Adversaires
    yellow_cards_against,
    red_cards_against,
    second_yellow_cards_against,
    fouls_committed_against,
    fouls_drawn_against,
    offsides_against,
    crosses_against,
    interceptions_against,
    tackles_won_against,
    own_goals_against

FROM {{ source('pau_fc', 'divers') }}
