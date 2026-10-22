
import pandas as pd

path = "data/raw/effectif_23-24.csv"

for encoding in ["utf-8-sig", "cp1252", "latin-1"]:
    try:
        df = pd.read_csv(path, encoding=encoding)

        print(f"{encoding} : {df['Player'].iloc[7]}")

    except UnicodeDecodeError:
        print(f"{encoding} : incompatible")
