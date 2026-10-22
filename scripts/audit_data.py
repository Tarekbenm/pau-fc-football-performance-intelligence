
from pathlib import Path
import csv
import pandas as pd


# Chemins du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"
REPORT_DIR = PROJECT_ROOT / "data" / "processed"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

csv_files = sorted(DATA_DIR.rglob("*.csv"))
results = []

print("=== AUDIT DES DONNÉES PAU FC ===")
print(f"Nombre de fichiers trouvés : {len(csv_files)}\n")


def detect_format(file_path):
    """Détecte l'encodage et le séparateur d'un fichier CSV."""

    for encoding in ["utf-8-sig", "cp1252", "latin-1"]:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                sample = f.read(8192)

            try:
                dialect = csv.Sniffer().sniff(
                    sample,
                    delimiters=",;\t"
                )
                separator = dialect.delimiter

            except csv.Error:
                separator = ","

            return encoding, separator

        except UnicodeDecodeError:
            continue

    raise ValueError("Encodage non reconnu")


# Audit des fichiers CSV
for file in csv_files:
    try:
        encoding, separator = detect_format(file)

        df = pd.read_csv(
            file,
            encoding=encoding,
            sep=separator,
            low_memory=False
        )

        # Contrôle des valeurs manquantes et des doublons
        missing_values = int(df.isna().sum().sum())
        duplicate_rows = int(df.duplicated().sum())

        results.append({
            "file": file.name,
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
            "encoding": encoding,
            "separator": repr(separator),
            "status": "OK"
        })

        print(
            f"{file.name} | "
            f"{len(df)} lignes | "
            f"{len(df.columns)} colonnes | "
            f"{missing_values} valeurs manquantes | "
            f"{duplicate_rows} doublons"
        )

    except Exception as error:
        print(f"ERREUR : {file.name} -> {error}")

        results.append({
            "file": file.name,
            "rows": None,
            "columns": None,
            "missing_values": None,
            "duplicate_rows": None,
            "encoding": None,
            "separator": None,
            "status": f"ERROR: {error}"
        })


# Génération du rapport d'audit
report = pd.DataFrame(results)

output_path = REPORT_DIR / "audit_report.csv"
report.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)


# Résumé
print("\n=== RÉSUMÉ DE L'AUDIT ===")
print(f"Fichiers analysés : {len(report)}")
print(f"Fichiers en erreur : {(report['status'] != 'OK').sum()}")
print(f"Rapport enregistré : {output_path}")

print("\nAudit terminé !")
