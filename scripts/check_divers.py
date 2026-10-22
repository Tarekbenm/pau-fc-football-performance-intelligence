
import pandas as pd

matches = pd.read_csv("data/processed/matches_clean.csv")
divers = pd.read_csv("data/processed/divers_clean.csv")

keys = ["season", "matchweek"]

print("Doublons :", divers.duplicated(keys).sum())

# Vérifier que chaque match possède ses statistiques
check = matches[keys].merge(
    divers[keys],
    on=keys,
    how="outer",
    indicator=True,
    validate="one_to_one",
)

print("\nCorrespondance des matchs :")
print(check["_merge"].value_counts())

# Vérifier les valeurs manquantes
print("\nValeurs manquantes par colonne :")
print(divers.isna().sum().to_string())

# Vérifier les valeurs négatives
stats = divers.drop(columns=keys)
print("\nValeurs négatives :", (stats < 0).sum().sum())
