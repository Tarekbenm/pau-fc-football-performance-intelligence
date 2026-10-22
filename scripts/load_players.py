import pandas as pd
from sqlalchemy import create_engine, text

# Connexion à PostgreSQL dans Docker
engine = create_engine(
    "postgresql+psycopg2://pau_fc:pau_fc_dev@localhost:5433/pau_fc"
)

# Charger les données nettoyées
players = pd.read_csv(
    "data/processed/players_clean.csv"
)

# Créer la table public.players
players.to_sql(
    "players",
    engine,
    schema="public",
    if_exists="replace",
    index=False,
)

# Vérifier le chargement
with engine.connect() as connection:
    count = connection.execute(
        text("SELECT COUNT(*) FROM public.players")
    ).scalar()

print(f"Joueurs-saisons chargés : {count}")
