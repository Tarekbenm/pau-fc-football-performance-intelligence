
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

SEASONS = ["23-24", "24-25", "25-26", "26-27"]

STATS = {
    "CrdY": "yellow_cards",
    "CrdR": "red_cards",
    "2CrdY": "second_yellow_cards",
    "Fls": "fouls_committed",
    "Fld": "fouls_drawn",
    "Off": "offsides",
    "Crs": "crosses",
    "Int": "interceptions",
    "TklW": "tackles_won",
    "OG": "own_goals",
}


def load_csv(path):
    for encoding in ["utf-8-sig", "cp1252", "latin-1"]:
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue


def clean_divers(df, season, side):
    df = df.copy()

    # Garder uniquement les journées de Ligue 2
    if "Comp" in df.columns:
        df = df[df["Comp"] == "Ligue 2"]

    df = df[
        df["Round"].astype(str).str.match(r"^Matchweek \d+$")
    ].copy()

    df["season"] = f"20{season[:2]}-20{season[-2:]}"
    df["matchweek"] = df["Round"].str.extract(r"(\d+)").astype(int)

    # Distinguer Pau FC et ses adversaires
    rename_columns = {
        column: f"{name}_{side}"
        for column, name in STATS.items()
    }

    df = df.rename(columns=rename_columns)

    columns = [
        "season",
        "matchweek",
        *rename_columns.values(),
    ]

    return df[columns]


all_seasons = []

for season in SEASONS:
    pau = clean_divers(
        load_csv(RAW_DIR / f"divers_stats_for_{season}.csv"),
        season,
        "for",
    )

    opponents = clean_divers(
        load_csv(RAW_DIR / f"divers_stats_against_{season}.csv"),
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

divers = pd.concat(all_seasons, ignore_index=True)

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

divers.to_csv(
    PROCESSED_DIR / "divers_clean.csv",
    index=False,
)

print(f"Matchs nettoyés : {len(divers)}")
print(divers.groupby("season").size())
print(divers.head().to_string(index=False))
