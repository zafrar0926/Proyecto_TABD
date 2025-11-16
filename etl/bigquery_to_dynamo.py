# ===============================================================
# PROYECTO F1 - ETL BigQuery → DynamoDB (versión para Streamlit)
# ===============================================================

import json
import boto3
import pandas as pd
from google.cloud import bigquery
from botocore.exceptions import ClientError
from datetime import datetime
import os
import csv
import math
from decimal import Decimal

# -------------------------------
# CONFIGURACIÓN
# -------------------------------
PROJECT_ID = "topicos-bases-datos"
DATASET = "f1_data_warehouse"
TABLE = "santi_perfil_conducto_agregado_dynamodb"
DYNAMO_TABLE = "perfiles_pilotos"
REGION = "us-east-1"

# -------------------------------
# SANITIZAR DATOS PARA DYNAMO
# -------------------------------
def sanitize_item(obj):
    if isinstance(obj, list):
        return [sanitize_item(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: sanitize_item(v) for k, v in obj.items()}
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return Decimal(str(round(obj, 4)))
    return obj


# ===============================================================
# 🚀 FUNCIÓN PRINCIPAL PARA STREAMLIT
# ===============================================================
def run_bigquery_to_dynamo():

    # -------------------------------
    # CREDENCIALES GOOGLE BIGQUERY
    # -------------------------------
    GOOGLE_CREDENTIALS_PATH = r"C:\Users\santi\Downloads\Learning\Maestria\Topicos Avanzados en Bases de Datos\Proyecto Final\Entrega\Core\2. From_Mongo_to_BigQuery\topicos-bases-datos-0af108d2076b.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_PATH

    # -------------------------------
    # CARGAR CREDENCIALES AWS DESDE CSV
    # -------------------------------
    CSV_PATH = r"C:\Users\santi\Downloads\Learning\Maestria\Topicos Avanzados en Bases de Datos\Proyecto Final\Entrega\Core\3. From Bigquery_to_Dynamo\bq-dynamodb-writer_accessKeys.csv"

    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        keys = next(reader)

    access_col = next((c for c in keys.keys() if "access" in c.lower() and "id" in c.lower()), None)
    secret_col = next((c for c in keys.keys() if "secret" in c.lower()), None)

    AWS_ACCESS_KEY = keys[access_col]
    AWS_SECRET_KEY = keys[secret_col]

    # -------------------------------
    # CONEXIONES
    # -------------------------------
    bq_client = bigquery.Client(project=PROJECT_ID)

    dynamo = boto3.resource(
        "dynamodb",
        region_name=REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    table = dynamo.Table(DYNAMO_TABLE)

    # -------------------------------
    # QUERY A BIGQUERY
    # -------------------------------
    query = f"""
    SELECT 
      DriverID,
      team,
      tyreManagementIndex,
      consistencyScore,
      sectorPerformanceProfile,
      preferredCompound,
      bestTrack,
      wetWeatherRating
    FROM `{PROJECT_ID}.{DATASET}.{TABLE}`;
    """

    df = bq_client.query(query).to_dataframe()

    updated = 0

    for _, row in df.iterrows():
        item = {
            "DriverID": row["DriverID"],
            "team": row["team"],
            "tyreManagementIndex": row["tyreManagementIndex"],
            "consistencyScore": row["consistencyScore"],
            "sectorPerformanceProfile": json.loads(row["sectorPerformanceProfile"]),
            "preferredCompound": row["preferredCompound"],
            "bestTrack": row["bestTrack"],
            "wetWeatherRating": row["wetWeatherRating"],
            "updated_at": datetime.utcnow().isoformat()
        }

        item = sanitize_item(item)

        try:
            table.put_item(Item=item)
            updated += 1
        except Exception as e:
            return f"❌ Error cargando {row['DriverID']}: {e}"

    return f"✔ Carga completada: {updated} pilotos actualizados en DynamoDB"
