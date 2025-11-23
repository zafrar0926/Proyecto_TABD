"""
Componente de header principal
"""
import streamlit as st


def render_header():
    """Renderiza el header principal de la aplicación"""
    st.markdown("""
    <div class="main-header-container">
        <div>
            <div class="main-subtitle">RACE STRATEGY PLATFORM v3.0</div>
            <h1 class="main-title">MISSION CONTROL</h1>
        </div>
        <div style="text-align: right;">
            <span style="color: #666; font-size: 0.9rem;">LIVE TELEMETRY FEED</span><br>
            <span style="color: #FFF; font-weight: bold;">GP: ABU DHABI 2025</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
