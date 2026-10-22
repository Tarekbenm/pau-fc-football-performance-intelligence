
from pathlib import Path
import pandas as pd

raw_dir = Path("data/raw")

keywords = [
    "shooting",
    "goalkeeping",
    "divers_stats",
    "effectif",
    "stats_",
    "L2",
]

for file in sorted(raw_dir.glob("*.csv")):
    if not any(word.lower() in file.name.lower() for word in keywords):
        continue

    for encoding in ["utf-8-sig", "cp1252", "latin-1"]:
        try:
            df = pd.read_csv(file, encoding=encoding)
            break
        except UnicodeDecodeError:
            continue

    print(f"\n{'=' * 65}")
    print(f"Fichier : {file.name}")
    print(f"Lignes : {len(df)}")
    print(f"Colonnes ({len(df.columns)}) :")
    print(df.columns.tolist())
