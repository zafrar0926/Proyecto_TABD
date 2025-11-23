#!/bin/bash
# Script para iniciar el frontend Streamlit

cd "$(dirname "$0")/etl"
echo "🎨 Iniciando frontend Streamlit"
python3 -m streamlit run streamlit_app.py
