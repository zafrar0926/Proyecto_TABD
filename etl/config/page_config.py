"""
Configuración de página de Streamlit
"""
import streamlit as st


def setup_page():
    """Configura la página de Streamlit con título, layout e icono"""
    st.set_page_config(
        page_title="F1 Mission Control",
        layout="wide",
        page_icon="🏎️",
        initial_sidebar_state="expanded"
    )
