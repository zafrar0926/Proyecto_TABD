"""
Componente de sidebar para la aplicación
"""
import streamlit as st
from services.api_client import check_api_status
from config.constants import F1_LOGO_URL


def render_sidebar():
    """Renderiza el sidebar con logo, status de API y métricas"""
    with st.sidebar:
        # Logo F1
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="{F1_LOGO_URL}" width="80" style="opacity: 0.8;">
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🖥️ SYSTEM STATUS")

        # Check FastAPI status
        is_online, api_data = check_api_status()

        if is_online:
            st.markdown("""
            <div style="background: rgba(57, 255, 20, 0.1); border: 1px solid #39FF14; padding: 10px; border-radius: 4px; color: #39FF14; text-align: center; font-weight: bold; margin-bottom: 10px;">
                ● API ONLINE
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(255, 24, 1, 0.1); border: 1px solid #FF1801; padding: 10px; border-radius: 4px; color: #FF1801; text-align: center; font-weight: bold; margin-bottom: 10px;">
                ● API OFFLINE
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Métricas de la sesión
        if 'contador_ejecuciones' not in st.session_state:
            st.session_state.contador_ejecuciones = 0

        col_mini1, col_mini2 = st.columns(2)
        with col_mini1:
            st.metric("ETL Cycles", st.session_state.contador_ejecuciones)
        with col_mini2:
            st.metric("Latency", "12ms")  # Simulado para efecto

        st.markdown("---")

        # Información de arquitectura
        st.markdown("""
        <div style="font-size: 0.7rem; color: #666;">
            ARCHITECTURE:<br>
            > MongoDB Atlas (Raw)<br>
            > Google BigQuery (OLAP)<br>
            > AWS DynamoDB (KV)<br>
            > Looker Studio (BI)
        </div>
        """, unsafe_allow_html=True)
