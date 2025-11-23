from mongo_to_bigquery import run_mongo_to_bigquery
from transform_profiles import run_transform_profiles
from bigquery_to_dynamo import run_bigquery_to_dynamo

import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

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
# SECCIÓN 0: INGESTA AUTOMÁTICA
# ===========================
st.markdown("---")
st.subheader("🛠️ Ingesta Automática de Datos (Mongo → BigQuery → DynamoDB)")

# Inicializar estado de sesión
if 'ingesta_activa' not in st.session_state:
    st.session_state.ingesta_activa = False
if 'ultima_ejecucion' not in st.session_state:
    st.session_state.ultima_ejecucion = None
if 'contador_ejecuciones' not in st.session_state:
    st.session_state.contador_ejecuciones = 0
if 'ultimo_log' not in st.session_state:
    st.session_state.ultimo_log = []

# Año fijo para ingesta automática
INGESTA_YEAR = 2025
INTERVALO_SEGUNDOS = 30

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🚀 Activar Ingesta Automática", type="primary", disabled=st.session_state.ingesta_activa):
        st.session_state.ingesta_activa = True
        st.session_state.contador_ejecuciones = 0
        st.success(f"✅ Ingesta automática ACTIVADA (Año: {INGESTA_YEAR}, cada {INTERVALO_SEGUNDOS}s)")
        st.rerun()

with col2:
    if st.button("⏹️ Desactivar Ingesta Automática", type="secondary", disabled=not st.session_state.ingesta_activa):
        st.session_state.ingesta_activa = False
        st.session_state.ultimo_log = []
        st.warning("⏹️ Ingesta automática desactivada.")
        st.rerun()

# Mostrar estado actual
st.markdown("---")
col_status1, col_status2, col_status3 = st.columns(3)

with col_status1:
    if st.session_state.ingesta_activa:
        st.success(f"🟢 Estado: ACTIVA")
    else:
        st.info(f"🔴 Estado: INACTIVA")

with col_status2:
    st.metric("Ejecuciones totales", st.session_state.contador_ejecuciones)

with col_status3:
    if st.session_state.ultima_ejecucion:
        st.metric("Última ejecución", st.session_state.ultima_ejecucion)
    else:
        st.metric("Última ejecución", "N/A")

# Área de logs
log_container = st.container()

# Ejecutar ingesta si está activa
if st.session_state.ingesta_activa:
    with log_container:
        st.markdown("### 📋 Logs de Ejecución")

        try:
            # Mostrar hora de inicio
            hora_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.info(f"⏰ Iniciando ejecución #{st.session_state.contador_ejecuciones + 1} a las {hora_inicio}")

            # Paso 1: Cargar desde MongoDB a BigQuery
            with st.spinner(f"📥 Paso 1: Cargando datos del año {INGESTA_YEAR} desde MongoDB..."):
                result_mongo = run_mongo_to_bigquery(INGESTA_YEAR)
            st.success("✅ Paso 1 completado: Carga desde MongoDB")
            with st.expander("Ver detalles de MongoDB → BigQuery"):
                st.text(result_mongo)

            # Paso 2: Actualizar DynamoDB
            with st.spinner("📤 Paso 2: Actualizando DynamoDB..."):
                result_dynamo = run_bigquery_to_dynamo()
            st.success("✅ Paso 2 completado: DynamoDB actualizado")
            with st.expander("Ver detalles de BigQuery → DynamoDB"):
                st.text(result_dynamo)

            # Actualizar estado
            st.session_state.contador_ejecuciones += 1
            st.session_state.ultima_ejecucion = hora_inicio

            st.success(f"🎉 Ejecución #{st.session_state.contador_ejecuciones} completada exitosamente!")

            # Esperar 30 segundos antes de la próxima ejecución
            st.info(f"⏳ Esperando {INTERVALO_SEGUNDOS} segundos para la próxima ejecución...")
            time.sleep(INTERVALO_SEGUNDOS)

            # Recargar la página para ejecutar de nuevo
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error durante la ejecución #{st.session_state.contador_ejecuciones + 1}: {e}")
            st.warning("La ingesta automática continuará en el próximo ciclo...")

            # Actualizar contador incluso con error
            st.session_state.contador_ejecuciones += 1
            st.session_state.ultima_ejecucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Esperar y reintentar
            time.sleep(INTERVALO_SEGUNDOS)
            st.rerun()

else:
    with log_container:
        st.markdown("### 📋 Logs de Ejecución")
        st.info("⏸️ La ingesta automática está desactivada. Presiona 'Activar Ingesta Automática' para comenzar.")

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
