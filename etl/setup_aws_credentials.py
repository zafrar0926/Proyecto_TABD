#!/usr/bin/env python3
# ===============================================================
# Script para configurar credenciales AWS desde CSV
# ===============================================================
import os
import csv

def setup_aws_credentials():
    """Lee el CSV de credenciales y configura variables de entorno"""
    CSV_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "3. From Bigquery_to_Dynamo",
        "bq-dynamodb-writer_accessKeys.csv"
    )

    if not os.path.exists(CSV_PATH):
        print(f"❌ No se encontró el archivo de credenciales en: {CSV_PATH}")
        return False

    try:
        with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            keys = next(reader)

        access_col = next((c for c in keys.keys() if "access" in c.lower() and "id" in c.lower()), None)
        secret_col = next((c for c in keys.keys() if "secret" in c.lower()), None)

        os.environ["AWS_ACCESS_KEY_ID"] = keys[access_col]
        os.environ["AWS_SECRET_ACCESS_KEY"] = keys[secret_col]
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

        print("✅ Credenciales AWS configuradas correctamente")
        return True

    except Exception as e:
        print(f"❌ Error al configurar credenciales: {e}")
        return False

if __name__ == "__main__":
    setup_aws_credentials()
