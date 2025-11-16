from mongo_to_bigquery import run_mongo_to_bigquery
from transform_profiles import run_transform_profiles
from bigquery_to_dynamo import run_bigquery_to_dynamo

import streamlit as st
import requests
import pandas as pd

# ===========================
# CONFIGURACIÓN GENERAL
# ===========================
st.set_page_config(
    page_title="F1 Analytics Platform",
    layout="wide",
    page_icon="🏎️",
)

st.title("🏁 Plataforma de Análisis Estratégico - Fórmula 1")
st.markdown("### Integración BigQuery + Looker + DynamoDB + FastAPI")

# ===========================
# SECCIÓN 0: BOTONES ETL (arriba del todo)
# ===========================
st.markdown("---")
st.subheader("🛠️ ETL - Actualización de Datos (Mongo → BigQuery → DynamoDB)")

colA, colB, colC = st.columns(3)

# 0.1 Selección de Año
with colA:
    st.markdown("### 📅 Año a cargar")
    load_year = st.number_input(
        "Selecciona el año",
        min_value=2018,
        max_value=2025,
        step=1,
        value=2023,
        key="load_year_input"
    )

# 0.2 Mongo → BigQuery
with colB:
    st.markdown("### 📥 Mongo → BigQuery")
    if st.button("Cargar año desde MongoDB"):
        with st.spinner(f"Cargando datos del año {load_year} desde MongoDB..."):
            result = run_mongo_to_bigquery(load_year)
        st.success("Carga completada.")
        st.text(result)

# 0.3 Transformación de perfiles
with colC:
    st.markdown("### 🔧 Transformación de Perfiles")
    if st.button("Crear perfiles de pilotos"):
        with st.spinner(f"Ejecutando transformación en BigQuery para {load_year}..."):
            result = run_transform_profiles(load_year)
        st.success("Transformación completada.")
        st.text(result)

# 0.4 BigQuery → DynamoDB debajo
colD, colE, colF = st.columns(3)
with colE:
    st.markdown("### 📤 BigQuery → DynamoDB")
    if st.button("Actualizar DynamoDB"):
        with st.spinner("Actualizando DynamoDB..."):
            result = run_bigquery_to_dynamo()
        st.success("DynamoDB actualizado.")
        st.text(result)

# ===========================
# SECCIÓN 1: Dashboard Looker
# ===========================
st.markdown("---")
st.subheader("📊 Dashboard Analítico (Looker)")

looker_url = st.text_input(
    "URL del Dashboard de Looker (iframe público)",
    "https://lookerstudio.google.com/embed/reporting/14b2dcfe-5a7e-49b2-8ecf-6f2e22d6051a/page/p_ealwatq5xd",
)

st.components.v1.html(
    f"""
    <iframe src="{looker_url}" width="100%" height="600" frameborder="0" allowfullscreen></iframe>
    """,
    height=620,
)

# ===========================
# SECCIÓN 2: Perfiles (FastAPI → DynamoDB)
# ===========================
st.subheader("🧠 Perfiles de Pilotos (DynamoDB vía FastAPI)")

API_URL = "http://127.0.0.1:8000/driver"

pilotos = [
    "VER", "HAM", "NOR", "LEC", "SAI", "PIA",
    "ALO", "STR", "RUS", "GAS", "OCO", "ALB"
]
selected_driver = st.selectbox("Selecciona un piloto", pilotos)

if st.button("🔍 Ver Perfil"):
    try:
        response = requests.get(f"{API_URL}/{selected_driver}")
        if response.status_code == 200:
            data = response.json()
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("🏎️ Piloto", selected_driver)
                st.metric("Equipo", data.get("team", "N/A"))
                st.metric("Pista Favorita", data.get("bestTrack", "N/A"))

            with col2:
                st.metric("🧩 Gestión de Neumáticos", data.get("tyreManagementIndex", "N/A"))
                st.metric("Consistencia", data.get("consistencyScore", "N/A"))

            with col3:
                st.metric("🌧️ Rendimiento en Lluvia", data.get("wetWeatherRating", "N/A"))
                st.json(data.get("sectorPerformanceProfile", {}))

        else:
            st.error(f"Error {response.status_code}: No se pudo obtener el perfil del piloto.")
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")

# ===========================
# SECCIÓN 3: Estado del Sistema
# ===========================
st.markdown("---")
st.subheader("⚙️ Estado del Sistema")

colA, colB = st.columns(2)
with colA:
    st.info("**FastAPI Status Endpoint:**")
    try:
        status = requests.get("http://127.0.0.1:8000/").json()
        st.json(status)
    except:
        st.warning("No se pudo conectar al endpoint de estado.")

with colB:
    st.success("**Arquitectura:** BigQuery → Looker → DynamoDB → FastAPI → Streamlit")
