
import pandas as pd

matches = pd.read_csv("data/processed/matches_clean.csv")
shooting = pd.read_csv("data/processed/shooting_clean.csv")

keys = ["season", "matchweek"]

# Vérifier les doublons
print("Doublons matchs :", matches.duplicated(keys).sum())
print("Doublons tirs :", shooting.duplicated(keys).sum())

# Identifier les matchs sans statistiques de tirs
check = matches[keys].merge(
    shooting[keys],
    on=keys,
    how="outer",
    indicator=True,
    validate="one_to_one",
)

print("\nCorrespondance des matchs :")
print(check["_merge"].value_counts())

# Vérifier les valeurs incohérentes
invalid = shooting[
    (shooting["shots_on_target_for"] > shooting["shots_for"])
    | (shooting["shots_on_target_against"] > shooting["shots_against"])
    | (shooting["shots_for"] < 0)
    | (shooting["shots_against"] < 0)
]

print("\nLignes avec statistiques incohérentes :", len(invalid))
