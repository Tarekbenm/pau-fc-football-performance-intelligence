
from pathlib import Path
import re
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
OUTPUT_DIR = ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = {
    "2023-2024": "Scores & Fixtures 23-24.csv",
    "2024-2025": "Scores & Fixtures 24-25.csv",
    "2025-2026": "Scores & Fixtures 25-26.csv",
    "2026-2027": "Scores & Fixtures 26-27.csv"
}

columns = [
    "Date", "Round", "Venue", "Result",
    "GF", "GA", "Opponent", "Poss",
    "Formation", "Opp Formation"
]

matches = []

for season, filename in files.items():
    file_path = RAW_DIR / filename

    # Lecture des fichiers
    df = pd.read_csv(file_path, encoding="latin-1")

    # Filtre Ligue 2 si la compétition est renseignée
    if "Comp" in df.columns:
        df = df[df["Comp"] == "Ligue 2"].copy()

    # Vérification des journées de championnat
    rounds = df["Round"].astype(str).str.extract(r"^Matchweek (\d+)$")[0]

    if rounds.isna().any():
        raise ValueError(f"Journées non reconnues : {filename}")

    df["matchweek"] = rounds.astype(int)

    if df["matchweek"].duplicated().any():
        raise ValueError(f"Journées en double : {filename}")

    expected_rounds = set(range(1, 39 if season == "2023-2024" else 35))
    actual_rounds = set(df["matchweek"])

    if season != "2026-2027" and actual_rounds != expected_rounds:
        raise ValueError(f"Journées manquantes : {filename}")

    # Sélection des colonnes utiles
    df = df[columns + ["matchweek"]].copy()

    df["season"] = season

    matches.append(df)

# Regroupement des quatre saisons
matches_clean = pd.concat(matches, ignore_index=True)

# Harmonisation des noms de colonnes
matches_clean = matches_clean.rename(columns={
    "Date": "match_date",
    "Venue": "venue",
    "Result": "result",
    "GF": "goals_for",
    "GA": "goals_against",
    "Opponent": "opponent",
    "Poss": "possession",
    "Formation": "formation",
    "Opp Formation": "opponent_formation"
})

matches_clean = matches_clean.drop(columns=["Round"])

# Conversion des types
matches_clean["match_date"] = pd.to_datetime(
    matches_clean["match_date"], errors="raise"
)

for col in ["goals_for", "goals_against", "possession"]:
    matches_clean[col] = pd.to_numeric(
        matches_clean[col], errors="raise"
    )

# Indicateurs de performance
matches_clean["points"] = matches_clean["result"].map({
    "W": 3,
    "D": 1,
    "L": 0
})

if matches_clean["points"].isna().any():
    raise ValueError("Résultat de match non reconnu")

matches_clean["goal_difference"] = (
    matches_clean["goals_for"] - matches_clean["goals_against"]
)

# Contrôles de qualité
if matches_clean.duplicated(["season", "matchweek"]).any():
    raise ValueError("Doublons saison / journée")

if (matches_clean[["goals_for", "goals_against"]] < 0).any().any():
    raise ValueError("Nombre de buts négatif")

if (~matches_clean["possession"].between(0, 100)).any():
    raise ValueError("Possession invalide")

# Export
output_path = OUTPUT_DIR / "matches_clean.csv"

matches_clean = matches_clean.sort_values(
    ["season", "matchweek"]
)

matches_clean.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

print("=== NETTOYAGE TERMINÉ ===")
print(f"Matchs conservés : {len(matches_clean)}")
print(matches_clean.groupby("season").size())
print(f"Fichier généré : {output_path}")
