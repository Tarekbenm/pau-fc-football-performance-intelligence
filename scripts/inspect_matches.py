
from pathlib import Path
import pandas as pd

# Chemins
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "raw"

# Analyse des calendriers et résultats du Pau FC
files = sorted(DATA_DIR.glob("Scores & Fixtures*.csv"))

for file in files:
   # Lecture des CSV avec plusieurs encodages possibles
    for encoding in ["utf-8-sig", "cp1252", "latin-1"]:
        try:
            df = pd.read_csv(file, encoding=encoding)
            print(f"Encodage utilisé : {encoding}")
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError(f"Impossible de lire {file.name}")

    print(f"\n{'=' * 60}")
    print(f"Fichier : {file.name}")
    print(f"Dimensions : {df.shape}")

    # Colonnes disponibles
    print("\nColonnes :")
    print(df.columns.tolist())

    # Aperçu des premières et dernières lignes
    print("\nPremières lignes :")
    print(df.head(3).to_string(index=False))

    print("\nDernières lignes :")
    print(df.tail(3).to_string(index=False))

    # Valeurs manquantes par colonne
    print("\nValeurs manquantes :")
    print(df.isna().sum()[df.isna().sum() > 0])
    
    # Vérification des compétitions en 2023-2024
    file = DATA_DIR / "Scores & Fixtures 23-24.csv"

    df = pd.read_csv(file, encoding="latin-1")

    print("\nCompétitions présentes :")
    print(df["Comp"].value_counts(dropna=False))

    print("\nMatchs hors Ligue 2 :")
    print(
        df.loc[df["Comp"] != "Ligue 2",
            ["Date", "Comp", "Opponent", "Result", "GF", "GA"]]
        .to_string(index=False)
    )
