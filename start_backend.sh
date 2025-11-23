#!/bin/bash
# Script para iniciar el backend FastAPI

cd "$(dirname "$0")/etl"
echo "🚀 Iniciando backend FastAPI en http://localhost:8000"
python3 -m uvicorn fast_api_app:app --reload --host 0.0.0.0 --port 8000
