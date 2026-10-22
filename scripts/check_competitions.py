
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw"

files = sorted(DATA_DIR.glob("Scores & Fixtures*.csv"))

for file in files:
    # Lecture des fichiers
    df = pd.read_csv(file, encoding="latin-1")

    print(f"\n=== {file.name} ===")
    print(f"Nombre de matchs : {len(df)}")

    if "Comp" in df.columns:
        print(df["Comp"].value_counts(dropna=False))
    else:
        print("Colonne Comp absente")

    # Vérification des journées
    print(f"Journées différentes : {df['Round'].nunique()}")
    print(f"Première journée : {df['Round'].iloc[0]}")
    print(f"Dernière journée : {df['Round'].iloc[-1]}")
