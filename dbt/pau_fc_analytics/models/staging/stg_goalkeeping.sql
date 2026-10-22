
SELECT
    season,
    matchweek,

    -- Gardiens du Pau FC
    shots_on_target_faced_for AS gk_shots_faced,
    goals_conceded_gk_for AS gk_goals_conceded,
    saves_for AS gk_saves,
    save_pct_for AS gk_save_pct,
    clean_sheets_gk_for AS gk_clean_sheet,
    penalties_faced_for AS gk_penalties_faced,
    penalties_conceded_for AS gk_penalties_conceded,
    penalties_saved_for AS gk_penalties_saved,

    -- Gardiens adverses
    shots_on_target_faced_against AS opponent_gk_shots_faced,
    goals_conceded_gk_against AS opponent_gk_goals_conceded,
    saves_against AS opponent_gk_saves,
    save_pct_against AS opponent_gk_save_pct

FROM {{ source('pau_fc', 'goalkeeping') }}
