
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


def clean_shooting(df, season, side):
    df = df.copy()

    # Conserver uniquement les matchs de championnat
    if "Comp" in df.columns:
        df = df[df["Comp"] == "Ligue 2"]

    df = df[df["Round"].astype(str).str.match(r"^Matchweek \d+$")].copy()

    df["season"] = f"20{season[:2]}-20{season[-2:]}"
    df["matchweek"] = df["Round"].str.extract(r"(\d+)").astype(int)

    df = df.rename(
        columns={
            "Sh": f"shots_{side}",
            "SoT": f"shots_on_target_{side}",
            "PK": f"penalty_goals_{side}",
            "PKatt": f"penalty_attempts_{side}",
        }
    )

    columns = [
        "season",
        "matchweek",
        f"shots_{side}",
        f"shots_on_target_{side}",
        f"penalty_goals_{side}",
        f"penalty_attempts_{side}",
    ]

    return df[columns]


all_seasons = []

for season in SEASONS:
    for_file = RAW_DIR / f"shooting_for_{season}.csv"
    against_file = RAW_DIR / f"shooting_against_{season}.csv"

    shots_for = clean_shooting(load_csv(for_file), season, "for")
    shots_against = clean_shooting(load_csv(against_file), season, "against")

    merged = shots_for.merge(
        shots_against,
        on=["season", "matchweek"],
        how="inner",
        validate="one_to_one",
    )

    all_seasons.append(merged)

shooting = pd.concat(all_seasons, ignore_index=True)

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
shooting.to_csv(PROCESSED_DIR / "shooting_clean.csv", index=False)

print(f"Matchs nettoyés : {len(shooting)}")
print(shooting.groupby("season").size())
print(shooting.head())
