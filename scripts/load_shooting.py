
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

CSV_PATH = Path("data/processed/shooting_clean.csv")

engine = create_engine(
    "postgresql+psycopg2://pau_fc:pau_fc_dev@localhost:5433/pau_fc"
)

shooting = pd.read_csv(CSV_PATH)

# Charger les statistiques de tirs dans PostgreSQL
shooting.to_sql(
    "shooting",
    engine,
    schema="public",
    if_exists="replace",
    index=False,
)

# Vérifier le nombre de matchs chargés
with engine.connect() as connection:
    count = connection.execute(
        text("SELECT COUNT(*) FROM public.shooting")
    ).scalar()

print(f"Matchs chargés dans PostgreSQL : {count}")
