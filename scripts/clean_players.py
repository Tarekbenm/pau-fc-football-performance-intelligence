
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
OUTPUT = Path("data/processed/players_clean.csv")

SEASONS = {
    "23-24": "2023-2024",
    "24-25": "2024-2025",
    "25-26": "2025-2026",
    "26-27": "2026-2027",
}

COLUMNS = {
    "-9999": "player_id",
    "Player": "player_name",
    "Nation": "nationality",
    "Pos": "position",
    "MP": "matches_played",
    "Starts": "starts",
    "Min": "minutes_played",
    "90s": "nineties",
    "Gls": "goals",
    "Ast": "assists",
    "G+A": "goal_contributions",
    "G-PK": "non_penalty_goals",
    "PK": "penalty_goals",
    "PKatt": "penalty_attempts",
    "CrdY": "yellow_cards",
    "CrdR": "red_cards",
    "Gls.1": "goals_per90",
    "Ast.1": "assists_per90",
    "G+A.1": "goal_contributions_per90",
    "G-PK.1": "non_penalty_goals_per90",
    "G+A-PK": "non_penalty_contributions_per90",
}


def load_csv(path):
    for encoding in ["utf-8-sig", "cp1252", "latin-1"]:
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue


all_players = []

for short_season, season in SEASONS.items():
    path = RAW_DIR / f"effectif_{short_season}.csv"
    df = load_csv(path)

    # Supprimer les lignes de total
    df = df[
        ~df["Player"].isin(["Squad Total", "Opponent Total"])
    ].copy()

    # Ajouter la saison
    df["season"] = season

    # Harmoniser l'âge : 36-323 devient 36
    df["age"] = pd.to_numeric(
        df["Age"].astype(str).str.split("-").str[0],
        errors="coerce",
    )

    # Renommer les colonnes
    df = df.rename(columns=COLUMNS)
    
    # Corrections des noms mal encodés
    name_corrections = {
        "Khalid Bouta‹b": "Khalid Boutaïb",
        "FidŠle Bongelo": "Fidèle Bongelo",
        "Ta‹ryk Arconte": "Taïryk Arconte",
    }

    df["player_name"] = df["player_name"].replace(name_corrections)

    # Les joueurs sans apparition ont 0 minute
    mask = (
        (df["matches_played"] == 0)
        & df["minutes_played"].isna()
    )
    df.loc[mask, "minutes_played"] = 0
    
    
    # Mettre à 0 les statistiques cumulées des joueurs sans match
    cumulative_stats = [
        "nineties",
        "goals",
        "assists",
        "goal_contributions",
        "non_penalty_goals",
        "penalty_goals",
        "penalty_attempts",
        "yellow_cards",
        "red_cards",
    ]

    no_appearance = df["matches_played"] == 0

    df.loc[no_appearance, cumulative_stats] = (
        df.loc[no_appearance, cumulative_stats].fillna(0)
    )


    # Garder uniquement les colonnes utiles
    df = df[
        ["season", "player_id", "player_name",
         "nationality", "position", "age",
         *[col for col in COLUMNS.values()
           if col not in [
               "player_id", "player_name",
               "nationality", "position"
           ]]]
    ]

    all_players.append(df)

players = pd.concat(all_players, ignore_index=True)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
players.to_csv(OUTPUT, index=False)

print("Nombre de lignes :", len(players))
print("\nJoueurs par saison :")
print(players.groupby("season").size())

print("\nDoublons joueur-saison :")
print(players.duplicated(["season", "player_id"]).sum())

print("\nAperçu :")
print(
    players[
        ["season", "player_name", "position",
         "minutes_played", "goals", "assists"]
    ].head(10).to_string(index=False)
)
