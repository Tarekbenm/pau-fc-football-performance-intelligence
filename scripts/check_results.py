
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / "data" / "processed" / "matches_clean.csv"

df = pd.read_csv(FILE)

# Bilan des points par saison
print("\n=== POINTS PAR SAISON ===")
print(df.groupby("season")["points"].sum())

# Nombre de matchs par saison
print("\n=== MATCHS PAR SAISON ===")
print(df.groupby("season").size())
