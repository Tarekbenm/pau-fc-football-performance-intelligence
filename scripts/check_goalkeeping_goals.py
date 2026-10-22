
import pandas as pd

matches = pd.read_csv("data/processed/matches_clean.csv")
goalkeeping = pd.read_csv("data/processed/goalkeeping_clean.csv")

df = matches.merge(
    goalkeeping,
    on=["season", "matchweek"],
    how="inner",
    validate="one_to_one",
)

# Comparer les buts encaissés par les gardiens
# avec les buts encaissés par chaque équipe
df["difference_goals_pau"] = (
    df["goals_against"] - df["goals_conceded_gk_for"]
)

df["difference_goals_opponents"] = (
    df["goals_for"] - df["goals_conceded_gk_against"]
)

goals_diff = df[
    (df["difference_goals_pau"] != 0)
    | (df["difference_goals_opponents"] != 0)
]

print("Matchs avec écarts de buts :", len(goals_diff))

print(
    goals_diff[
        [
            "season",
            "matchweek",
            "goals_against",
            "goals_conceded_gk_for",
            "goals_for",
            "goals_conceded_gk_against",
        ]
    ].head(15).to_string(index=False)
)

# Contrôler les arrêts par rapport aux tirs cadrés subis
for side in ["for", "against"]:
    difference = (
        df[f"shots_on_target_faced_{side}"]
        - df[f"goals_conceded_gk_{side}"]
        - df[f"saves_{side}"]
    )

    print(
        f"Écarts tirs cadrés - buts - arrêts ({side}) :",
        (difference != 0).sum(),
    )
