
import pandas as pd

players = pd.read_csv("data/processed/players_clean.csv")

print("Nombre de lignes :", len(players))

print("\nValeurs manquantes :")
print(players.isna().sum().to_string())

print("\nDoublons joueur-saison :")
print(players.duplicated(["season", "player_id"]).sum())

# Vérifier les statistiques de temps de jeu
print("\nMinutes négatives :")
print((players["minutes_played"] < 0).sum())

print("\nTitularisations supérieures aux matchs :")
print((players["starts"] > players["matches_played"]).sum())

# Vérifier les contributions offensives
print("\nIncohérences buts + passes :")
print(
    (
        players["goals"] + players["assists"]
        != players["goal_contributions"]
    ).sum()
)

# Vérifier les identifiants présents sur plusieurs saisons
print("\nJoueurs présents sur plusieurs saisons :")
print(
    players.groupby("player_id")["season"]
    .nunique()
    .loc[lambda x: x > 1]
    .count()
)

# Repérer les joueurs sans temps de jeu
print("\nJoueurs à 0 minute :")
print((players["minutes_played"] == 0).sum())


# Examiner les joueurs dont les buts sont manquants
missing = players[players["goals"].isna()]

print("\nJoueurs avec statistiques manquantes :")
print(
    missing[
        ["season", "player_name", "matches_played",
         "minutes_played", "goals", "assists"]
    ].to_string(index=False)
)

print("\nStatistiques manquantes avec minutes > 0 :")
print(
    (
        players["goals"].isna()
        & (players["minutes_played"] > 0)
    ).sum()
)

