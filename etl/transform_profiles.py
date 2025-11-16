# ===============================================================
# 🚀 PROYECTO F1 - BigQuery Transform → Tabla final Dynamo
# ===============================================================
# Este script:
# 1. Recibe un LOAD_YEAR
# 2. Genera o reemplaza la tabla santi_perfil_conducto_agregado_dynamodb
#    usando SOLO información desde 2021 hasta LOAD_YEAR
# ===============================================================

from google.cloud import bigquery
import os
from datetime import datetime

# -------------------------------
# CONFIG
# -------------------------------
PROJECT_ID = "topicos-bases-datos"
DATASET = "f1_data_warehouse"
DEST_TABLE = "santi_perfil_conducto_agregado_dynamodb"

GOOGLE_CREDENTIALS_PATH = r"C:\Users\santi\Downloads\Learning\Maestria\Topicos Avanzados en Bases de Datos\Proyecto Final\Entrega\Core\2. From_Mongo_to_BigQuery\topicos-bases-datos-0af108d2076b.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS_PATH

# ===============================================================
# FUNCIÓN PRINCIPAL — NOMBRE ESTÁNDAR
# ===============================================================
def run_transform_profiles(load_year: int):
    print(f"[{datetime.now()}] Ejecutando transform para el año {load_year}...")

    client = bigquery.Client(project=PROJECT_ID)

    sql = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET}.{DEST_TABLE}` AS
    WITH
    tyre_wear AS (
      SELECT
        Driver AS DriverID,
        Team,
        AVG(TyreLife) AS avg_tyre_life,
        COUNT(DISTINCT CONCAT(EventName, "_", Year)) AS total_races
      FROM `{PROJECT_ID}.{DATASET}.laps_enriched`
      WHERE SessionName = 'Race'
        AND TyreLife IS NOT NULL
        AND Year <= {load_year}
        AND EventDate >= DATE('2021-01-01')
      GROUP BY ALL
    ),
    consistency AS (
      SELECT
        Driver AS DriverID,
        SAFE_DIVIDE(1, STDDEV(EXTRACT(SECOND FROM LapTime))) * 100 AS consistency_raw
      FROM `{PROJECT_ID}.{DATASET}.laps_enriched`
      WHERE SessionName = 'Race'
        AND LapTime IS NOT NULL
        AND Year <= {load_year}
        AND EventDate >= DATE('2021-01-01')
      GROUP BY ALL
    ),
    sector_perf AS (
      SELECT
        Driver AS DriverID,
        AVG(Sector1_Speed_Avg) AS s1_avg,
        AVG(Sector2_Speed_Avg) AS s2_avg,
        AVG(Sector3_Speed_Avg) AS s3_avg
      FROM `{PROJECT_ID}.{DATASET}.laps_enriched`
      WHERE SessionName = 'Race'
        AND Year <= {load_year}
        AND EventDate >= DATE('2021-01-01')
      GROUP BY ALL
    ),
    compound_pref AS (
      WITH compound_counts AS (
        SELECT
          Driver AS DriverID,
          Compound,
          COUNT(*) AS usage_count
        FROM `{PROJECT_ID}.{DATASET}.laps_enriched`
        WHERE SessionName = 'Race'
          AND Year <= {load_year}
          AND EventDate >= DATE('2021-01-01')
        GROUP BY ALL
      )
      SELECT
        DriverID,
        ARRAY_AGG(Compound ORDER BY usage_count DESC LIMIT 1)[OFFSET(0)] AS preferred_compound
      FROM compound_counts
      GROUP BY ALL
    ),
    best_track AS (
      WITH avg_lap_per_track AS (
        SELECT
          Driver AS DriverID,
          EventName,
          AVG(EXTRACT(SECOND FROM LapTime)) AS avg_lap_time
        FROM `{PROJECT_ID}.{DATASET}.laps_enriched`
        WHERE SessionName = 'Race'
          AND Year <= {load_year}
          AND EventDate >= DATE('2021-01-01')
        GROUP BY ALL
      )
      SELECT
        DriverID,
        ARRAY_AGG(EventName ORDER BY avg_lap_time ASC LIMIT 1)[OFFSET(0)] AS best_track
      FROM avg_lap_per_track
      GROUP BY ALL
    ),
    wet_perf AS (
      SELECT
        l.Driver AS DriverID,
        CORR(CAST(IF(w.Rainfall, 1, 0) AS FLOAT64), EXTRACT(SECOND FROM l.LapTime)) AS corr_rain_laptime
      FROM `{PROJECT_ID}.{DATASET}.laps_enriched` AS l
      JOIN `{PROJECT_ID}.{DATASET}.weather` AS w
      USING (EventName, Year, SessionName)
      WHERE w.Rainfall IS NOT NULL
        AND l.SessionName = 'Race'
        AND l.LapTime IS NOT NULL
        AND Year <= {load_year}
        AND l.EventDate >= DATE('2021-01-01')
      GROUP BY ALL
    )
    SELECT
      t.DriverID,
      ANY_VALUE(t.Team) AS team,
      ROUND((t.avg_tyre_life / 30) * 10, 2) AS tyreManagementIndex,
      ROUND(c.consistency_raw, 2) AS consistencyScore,
      JSON_OBJECT(
        'high_speed', CASE WHEN (s1_avg + s2_avg + s3_avg)/3 > 200 THEN 'Elite'
                           WHEN (s1_avg + s2_avg + s3_avg)/3 > 160 THEN 'Above Average'
                           ELSE 'Average' END,
        'medium_speed', CASE WHEN s2_avg BETWEEN 150 AND 180 THEN 'Above Average' ELSE 'Average' END,
        'low_speed', CASE WHEN s3_avg < 150 THEN 'Strong' ELSE 'Average' END
      ) AS sectorPerformanceProfile,
      ANY_VALUE(cp.preferred_compound) AS preferredCompound,
      ANY_VALUE(bt.best_track) AS bestTrack,
      ROUND(10 - (ABS(ANY_VALUE(wp.corr_rain_laptime)) * 10), 2) AS wetWeatherRating
    FROM tyre_wear t
    LEFT JOIN consistency c USING (DriverID)
    LEFT JOIN sector_perf s USING (DriverID)
    LEFT JOIN compound_pref cp USING (DriverID)
    LEFT JOIN best_track bt USING (DriverID)
    LEFT JOIN wet_perf wp USING (DriverID)
    GROUP BY
      t.DriverID,
      t.avg_tyre_life,
      c.consistency_raw,
      s1_avg,s2_avg,s3_avg,
      cp.preferred_compound,
      bt.best_track,
      wp.corr_rain_laptime;
    """

    client.query(sql).result()

    print(f"[{datetime.now()}] 🚀 Transformación BigQuery completada ✔")

    return f"Tabla {DEST_TABLE} generada correctamente para {load_year}"
