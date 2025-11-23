"""
F1 Mission Control - Aplicación Principal
Streamlit dashboard para análisis de datos de Fórmula 1

Estructura del proyecto:
- config/: Configuraciones y constantes
- styles/: Estilos CSS personalizados
- components/: Componentes reutilizables (sidebar, header)
- tabs/: Tabs principales de la aplicación
- services/: Servicios para comunicación con APIs
"""

import streamlit as st

# Configuración de página (debe ser lo primero)
from config import setup_page
setup_page()

# Estilos
from styles import get_custom_css

# Componentes
from components import render_sidebar, render_header

# Tabs
from tabs import render_telemetry_tab, render_driver_intel_tab, render_pipeline_tab


def main():
    """Función principal de la aplicación"""

    # Aplicar CSS personalizado
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # Renderizar sidebar
    render_sidebar()

    # Renderizar header principal
    render_header()

    # Crear tabs principales
    tab1, tab2, tab3 = st.tabs([
        "📊 LIVE TELEMETRY",
        "🏎️ DRIVER INTEL",
        "⚙️ DATA PIPELINE"
    ])

    # Renderizar contenido de cada tab
    with tab1:
        render_telemetry_tab()

    with tab2:
        render_driver_intel_tab()

    with tab3:
        render_pipeline_tab()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #444; font-size: 0.7rem; font-family: 'Titillium Web'; letter-spacing: 1px;">
        SCUDERIA ANALYTICS // CLASSIFIED INFORMATION // v3.2.0-STABLE
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
