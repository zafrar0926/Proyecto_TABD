# ===============================================================
# PROYECTO F1 - API REST Local (FastAPI + DynamoDB)
# ---------------------------------------------------------------
# Objetivo: Servir perfiles de pilotos (perfiles_pilotos)
# obtenidos desde DynamoDB.
# ===============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import json
from setup_aws_credentials import setup_aws_credentials

# -------------------------------
# Configuración de credenciales
# -------------------------------
setup_aws_credentials()

# -------------------------------
# Configuración
# -------------------------------
AWS_REGION = "us-east-1"        # <- misma región que tu tabla DynamoDB
TABLE_NAME = "perfiles_pilotos"  # <- nombre exacto de la tabla
app = FastAPI(title="F1 Driver Profiles API", version="1.0")

# Inicializar cliente DynamoDB
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)


# -------------------------------
# Modelos de respuesta
# -------------------------------
class SectorProfile(BaseModel):
    high_speed: str
    medium_speed: str
    low_speed: str


class DriverProfile(BaseModel):
    DriverID: str
    team: str
    tyreManagementIndex: float
    consistencyScore: float
    sectorPerformanceProfile: SectorProfile
    preferredCompound: str
    bestTrack: str
    wetWeatherRating: float
    updated_at: str


# -------------------------------
# Utilidad para convertir Decimal → float
# -------------------------------
def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj


# -------------------------------
# Rutas
# -------------------------------

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "F1 Driver Profiles API is running",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/driver/{driver_id}", response_model=DriverProfile)
def get_driver_profile(driver_id: str):
    """Consulta un piloto por su DriverID"""
    try:
        resp = table.query(
            KeyConditionExpression=Key("DriverID").eq(driver_id)
        )
        if not resp["Items"]:
            raise HTTPException(status_code=404, detail="Driver not found")

        item = convert_decimals(resp["Items"][0])
        return item

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error DynamoDB: {str(e)}")


@app.get("/drivers")
def list_drivers():
    """Lista los IDs de todos los pilotos disponibles"""
    scan = table.scan(ProjectionExpression="DriverID, team")
    return convert_decimals(scan["Items"])
