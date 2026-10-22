
from pathlib import Path
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

ROOT = Path(__file__).resolve().parent.parent
FILE = ROOT / "data" / "processed" / "matches_clean.csv"

# Connexion à PostgreSQL
db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("POSTGRES_USER", "pau_fc"),
    password=os.getenv("POSTGRES_PASSWORD", "pau_fc_dev"),
    host="localhost",
    port=5433,
    database=os.getenv("POSTGRES_DB", "pau_fc")
)

engine = create_engine(db_url)

# Lecture du fichier nettoyé
df = pd.read_csv(FILE, parse_dates=["match_date"])

# Chargement dans une table SQL
df.to_sql(
    name="matches",
    con=engine,
    schema="public",
    if_exists="replace",
    index=False
)

# Vérification du chargement
with engine.connect() as conn:
    count = conn.execute(
        text("SELECT COUNT(*) FROM public.matches")
    ).scalar_one()

print(f"Matchs chargés dans PostgreSQL : {count}")
