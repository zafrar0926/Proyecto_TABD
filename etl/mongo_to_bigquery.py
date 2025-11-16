# ===============================================================
# 🚀 PROYECTO F1 - MongoDB → BigQuery (Carga anual limpia)
# ===============================================================

import pandas as pd
from pymongo import MongoClient
from google.cloud import bigquery
from datetime import datetime
import os
import certifi

# ===============================================================
# 🔧 CONFIGURACIÓN GENERAL
# ===============================================================

MONGO_URI = "mongodb+srv://santiago_bigq_access:26092510@cluster0.otgxigz.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB = "f1_data_warehouse"
COLLECTIONS = ["laps_enriched", "race_control", "results", "weather"]

PROJECT_ID = "topicos-bases-datos"
DATASET = "f1_data_warehouse"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    r"C:\Users\santi\Downloads\Learning\Maestria\Topicos Avanzados en Bases de Datos\Proyecto Final\Entrega\Core\2. From_Mongo_to_BigQuery\topicos-bases-datos-0af108d2076b.json"
)

bq_client = bigquery.Client(project=PROJECT_ID)

mongo_client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where()
)

# ===============================================================
# 🧩 FUNCIONES DE LIMPIEZA
# ===============================================================

def parse_time(val):
    if pd.isna(val) or val == "":
        return None
    for fmt in ("%H:%M:%S.%f", "%H:%M:%S"):
        try:
            return datetime.strptime(val, fmt).time()
        except ValueError:
            continue
    return None


def parse_timestamp(val):
    if pd.isna(val) or val == "":
        return None
    try:
        return pd.to_datetime(val, errors="coerce")
    except Exception:
        return None


def clean_dataframe(df, collection_name):
    df = df.copy()

    string_time_fields = {
        "Sector1_Throttle_100_Time", "Sector1_Brake_Time", "Sector1_Throttle_Time", "Sector1_Coasting_Time",
        "Sector2_Throttle_100_Time", "Sector2_Brake_Time", "Sector2_Throttle_Time", "Sector2_Coasting_Time",
        "Sector3_Throttle_100_Time", "Sector3_Brake_Time", "Sector3_Throttle_Time", "Sector3_Coasting_Time"
    }

    for col in df.columns:
        if "Time" in col and col not in string_time_fields:
            df[col] = df[col].apply(parse_time)
        elif "Date" in col:
            if col == "LapStartDate":
                df[col] = pd.to_datetime(df[col], errors="coerce")
            else:
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.date
        elif "Timestamp" in col:
            df[col] = df[col].apply(parse_timestamp)
        elif df[col].dtype == object:
            df[col] = df[col].replace({"nan": None, "NaN": None, "": None})

    return df

# ===============================================================
# 📘 ESQUEMAS FIJOS
# ===============================================================

def schema_laps_enriched():
    return [
        bigquery.SchemaField("Time", "TIME"),
        bigquery.SchemaField("Driver", "STRING"),
        bigquery.SchemaField("DriverNumber", "INTEGER"),
        bigquery.SchemaField("LapTime", "TIME"),
        bigquery.SchemaField("LapNumber", "FLOAT"),
        bigquery.SchemaField("Stint", "FLOAT"),
        bigquery.SchemaField("PitOutTime", "TIME"),
        bigquery.SchemaField("PitInTime", "TIME"),
        bigquery.SchemaField("Sector1Time", "TIME"),
        bigquery.SchemaField("Sector2Time", "TIME"),
        bigquery.SchemaField("Sector3Time", "TIME"),
        bigquery.SchemaField("SpeedI1", "FLOAT"),
        bigquery.SchemaField("SpeedI2", "FLOAT"),
        bigquery.SchemaField("SpeedFL", "FLOAT"),
        bigquery.SchemaField("SpeedST", "FLOAT"),
        bigquery.SchemaField("IsPersonalBest", "BOOLEAN"),
        bigquery.SchemaField("Compound", "STRING"),
        bigquery.SchemaField("TyreLife", "FLOAT"),
        bigquery.SchemaField("FreshTyre", "BOOLEAN"),
        bigquery.SchemaField("Team", "STRING"),
        bigquery.SchemaField("LapStartTime", "TIME"),
        bigquery.SchemaField("LapStartDate", "TIMESTAMP"),
        bigquery.SchemaField("TrackStatus", "INTEGER"),
        bigquery.SchemaField("Position", "FLOAT"),
        bigquery.SchemaField("Deleted", "BOOLEAN"),
        bigquery.SchemaField("DeletedReason", "STRING"),
        bigquery.SchemaField("FastF1Generated", "BOOLEAN"),
        bigquery.SchemaField("IsAccurate", "BOOLEAN"),
        bigquery.SchemaField("Year", "INTEGER"),
        bigquery.SchemaField("EventName", "STRING"),
        bigquery.SchemaField("SessionName", "STRING"),
        bigquery.SchemaField("Country", "STRING"),
        bigquery.SchemaField("Location", "STRING"),
        bigquery.SchemaField("OfficialEventName", "STRING"),
        bigquery.SchemaField("EventDate", "DATE"),
        bigquery.SchemaField("EventFormat", "STRING"),
    ]


def schema_race_control():
    return [
        bigquery.SchemaField("Time", "TIMESTAMP"),
        bigquery.SchemaField("Category", "STRING"),
        bigquery.SchemaField("Message", "STRING"),
        bigquery.SchemaField("Status", "STRING"),
        bigquery.SchemaField("Flag", "STRING"),
        bigquery.SchemaField("Scope", "STRING"),
        bigquery.SchemaField("Sector", "FLOAT"),
        bigquery.SchemaField("RacingNumber", "INTEGER"),
        bigquery.SchemaField("Lap", "FLOAT"),
        bigquery.SchemaField("Year", "INTEGER"),
        bigquery.SchemaField("EventName", "STRING"),
        bigquery.SchemaField("SessionName", "STRING"),
    ]


def schema_results():
    return [
        bigquery.SchemaField("DriverNumber", "INTEGER"),
        bigquery.SchemaField("BroadcastName", "STRING"),
        bigquery.SchemaField("Abbreviation", "STRING"),
        bigquery.SchemaField("DriverId", "STRING"),
        bigquery.SchemaField("TeamName", "STRING"),
        bigquery.SchemaField("TeamColor", "STRING"),
        bigquery.SchemaField("TeamId", "STRING"),
        bigquery.SchemaField("FirstName", "STRING"),
        bigquery.SchemaField("LastName", "STRING"),
        bigquery.SchemaField("FullName", "STRING"),
        bigquery.SchemaField("HeadshotUrl", "STRING"),
        bigquery.SchemaField("CountryCode", "STRING"),
        bigquery.SchemaField("Position", "FLOAT"),
        bigquery.SchemaField("ClassifiedPosition", "STRING"),
        bigquery.SchemaField("GridPosition", "FLOAT"),
        bigquery.SchemaField("Q1", "STRING"),
        bigquery.SchemaField("Q2", "STRING"),
        bigquery.SchemaField("Q3", "STRING"),
        bigquery.SchemaField("Time", "TIME"),
        bigquery.SchemaField("Status", "STRING"),
        bigquery.SchemaField("Points", "FLOAT"),
        bigquery.SchemaField("Laps", "FLOAT"),
        bigquery.SchemaField("Year", "INTEGER"),
        bigquery.SchemaField("EventName", "STRING"),
        bigquery.SchemaField("SessionName", "STRING"),
    ]


def schema_weather():
    return [
        bigquery.SchemaField("Time", "TIME"),
        bigquery.SchemaField("AirTemp", "FLOAT"),
        bigquery.SchemaField("Humidity", "FLOAT"),
        bigquery.SchemaField("Pressure", "FLOAT"),
        bigquery.SchemaField("Rainfall", "BOOLEAN"),
        bigquery.SchemaField("TrackTemp", "FLOAT"),
        bigquery.SchemaField("WindDirection", "INTEGER"),
        bigquery.SchemaField("WindSpeed", "FLOAT"),
        bigquery.SchemaField("Year", "INTEGER"),
        bigquery.SchemaField("EventName", "STRING"),
        bigquery.SchemaField("SessionName", "STRING"),
    ]
# ===============================================================
# 📌 CONFIG DE TABLAS
# ===============================================================

TABLE_CONFIGS = {
    "laps_enriched": {"schema": schema_laps_enriched()},
    "race_control": {"schema": schema_race_control()},
    "results": {"schema": schema_results()},
    "weather": {"schema": schema_weather()},
}

# ===============================================================
# 🚀 FUNCIÓN PRINCIPAL PARAMETRIZABLE
# ===============================================================

def run_mongo_to_bigquery(load_year: int):
    logs = []

    LOAD_YEAR = load_year
    LOAD_DATE = f"{LOAD_YEAR}-01-01"   # SOLO si lo necesitas luego

    for collection_name in COLLECTIONS:
        logs.append(f"\n=== Procesando colección: {collection_name} ===")

        # -----------------------------------------------
        # 1. Leer Mongo solo ese año
        # -----------------------------------------------
        logs.append(f"📥 Leyendo MongoDB SOLO para el año {LOAD_YEAR} ...")

        mongo_filter = {"Year": LOAD_YEAR}
        mongo_docs = list(mongo_client[MONGO_DB][collection_name].find(mongo_filter))

        df = pd.json_normalize(mongo_docs)

        if df.empty:
            logs.append(f"⚠️ No hay datos de {collection_name} para el año {LOAD_YEAR}.")
            continue

        if "_id" in df.columns:
            df = df.drop(columns=["_id"])

        df = clean_dataframe(df, collection_name)

        # -----------------------------------------------
        # 2. DELETE del año en la tabla destino
        # -----------------------------------------------
        final_table = f"{PROJECT_ID}.{DATASET}.{collection_name}"

        logs.append(f"🗑️ Eliminando año {LOAD_YEAR} en {final_table}")

        if collection_name == "laps_enriched":
            delete_query = f"""
            DELETE FROM `{final_table}`
            WHERE EXTRACT(YEAR FROM EventDate) = {LOAD_YEAR};
            """
        else:
            delete_query = f"""
            DELETE FROM `{final_table}`
            WHERE Year = {LOAD_YEAR};
            """

        bq_client.query(delete_query).result()

        # -----------------------------------------------
        # 3. INSERT del año limpio
        # -----------------------------------------------
        logs.append(f"⬆️ Insertando {len(df)} filas en {final_table} ...")

        schema = TABLE_CONFIGS[collection_name]["schema"]

        job_config = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition="WRITE_APPEND",
        )

        bq_client.load_table_from_dataframe(df, final_table, job_config=job_config).result()

        logs.append(f"✅ Completado {collection_name}")

    logs.append("\n=== 🚀 MIGRACIÓN COMPLETADA ===")
    return "\n".join(logs)