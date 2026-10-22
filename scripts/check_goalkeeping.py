
import pandas as pd

shooting = pd.read_csv("data/processed/shooting_clean.csv")
goalkeeping = pd.read_csv("data/processed/goalkeeping_clean.csv")

keys = ["season", "matchweek"]

# Vérifier les doublons
print("Doublons goalkeeping :", goalkeeping.duplicated(keys).sum())

# Comparer les matchs des deux fichiers
df = shooting.merge(
    goalkeeping,
    on=keys,
    how="outer",
    indicator=True,
    validate="one_to_one",
)

print("\nCorrespondance des matchs :")
print(df["_merge"].value_counts())

# Les tirs cadrés adverses doivent correspondre
# aux tirs cadrés subis par les gardiens de Pau
df["difference_pau"] = (
    df["shots_on_target_against"]
    - df["shots_on_target_faced_for"]
)

# Même vérification pour les gardiens adverses
df["difference_opponents"] = (
    df["shots_on_target_for"]
    - df["shots_on_target_faced_against"]
)

differences = df[
    (df["difference_pau"] != 0)
    | (df["difference_opponents"] != 0)
]

print("\nMatchs avec des écarts :", len(differences))

print("\nÉcarts par saison :")
print(differences.groupby("season").size())

print("\nPremiers écarts :")
print(
    differences[
        [
            "season",
            "matchweek",
            "shots_on_target_against",
            "shots_on_target_faced_for",
            "difference_pau",
            "shots_on_target_for",
            "shots_on_target_faced_against",
            "difference_opponents",
        ]
    ].head(10).to_string(index=False)
)
