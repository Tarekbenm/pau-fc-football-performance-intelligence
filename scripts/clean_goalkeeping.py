
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

SEASONS = ["23-24", "24-25", "25-26", "26-27"]


def load_csv(path):
    for encoding in ["utf-8-sig", "cp1252", "latin-1"]:
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue


def clean_goalkeeping(df, season, side):
    df = df.copy()

    # Garder uniquement les matchs de Ligue 2
    if "Comp" in df.columns:
        df = df[df["Comp"] == "Ligue 2"]

    # Exclure la ligne de total de saison
    df = df[
        df["Round"].astype(str).str.match(r"^Matchweek \d+$")
    ].copy()

    df["season"] = f"20{season[:2]}-20{season[-2:]}"
    df["matchweek"] = df["Round"].str.extract(r"(\d+)").astype(int)

    df = df.rename(
        columns={
            "SoTA": f"shots_on_target_faced_{side}",
            "GA.1": f"goals_conceded_gk_{side}",
            "Saves": f"saves_{side}",
            "Save%": f"save_pct_{side}",
            "CS": f"clean_sheets_gk_{side}",
            "PKatt": f"penalties_faced_{side}",
            "PKA": f"penalties_conceded_{side}",
            "PKsv": f"penalties_saved_{side}",
        }
    )

    columns = [
        "season",
        "matchweek",
        f"shots_on_target_faced_{side}",
        f"goals_conceded_gk_{side}",
        f"saves_{side}",
        f"save_pct_{side}",
        f"clean_sheets_gk_{side}",
        f"penalties_faced_{side}",
        f"penalties_conceded_{side}",
        f"penalties_saved_{side}",
    ]

    return df[columns]


all_seasons = []

for season in SEASONS:
    pau = clean_goalkeeping(
        load_csv(RAW_DIR / f"goalkeeping_for_{season}.csv"),
        season,
        "for",
    )

    opponents = clean_goalkeeping(
        load_csv(RAW_DIR / f"goalkeeping_against_{season}.csv"),
        season,
        "against",
    )

    merged = pau.merge(
        opponents,
        on=["season", "matchweek"],
        how="inner",
        validate="one_to_one",
    )

    all_seasons.append(merged)

goalkeeping = pd.concat(all_seasons, ignore_index=True)

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

goalkeeping.to_csv(
    PROCESSED_DIR / "goalkeeping_clean.csv",
    index=False,
)

print(f"Matchs nettoyés : {len(goalkeeping)}")
print(goalkeeping.groupby("season").size())
print(goalkeeping.head())
