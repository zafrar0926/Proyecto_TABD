"""
Tab de inteligencia de pilotos - Datos de DynamoDB
"""
import streamlit as st
from services.api_client import get_driver_data
from config.constants import DRIVER_IMAGES, TEAM_COLORS


def render_sector_box(title: str, value: str) -> str:
    """
    Renderiza una caja de sector con colores semánticos

    Args:
        title: Título del sector
        value: Valor del rendimiento (Elite, Strong, etc.)

    Returns:
        HTML string del sector box
    """
    bg_color = "#1f242d"
    text_color = "#fff"
    border_color = "#333"

    if value == "Elite":
        border_color = "#FF1801"
        text_color = "#FF1801"
    elif value == "Strong":
        border_color = "#39FF14"
        text_color = "#39FF14"

    return f"""
    <div style="background: {bg_color}; border: 1px solid {border_color}; padding: 15px; border-radius: 4px; text-align: center;">
        <div style="font-size: 0.7rem; color: #888; margin-bottom: 5px;">{title}</div>
        <div style="font-family: 'Michroma'; font-size: 1.1rem; color: {text_color};">{value}</div>
    </div>
    """


def render_driver_panel(data: dict, selected_driver: str, team_color: str):
    """Renderiza el panel del piloto con información básica"""
    st.markdown(f"""
    <div class="driver-panel" style="border-left-color: {team_color};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 class="driver-name">{data.get('fullName', selected_driver)}</h2>
                <div class="team-name" style="color: {team_color};">{data.get('team', 'Unknown Team')}</div>
            </div>
            <div style="text-align: right;">
                 <div style="font-family: 'Michroma'; font-size: 3rem; color: rgba(255,255,255,0.1);">#{selected_driver}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_driver_image_and_best_track(driver_img: str, best_track: str, team_color: str):
    """Renderiza la imagen del piloto y su pista favorita"""
    st.image(driver_img, use_container_width=True)
    st.markdown(f"""
    <div class="metric-card" style="border-top-color: {team_color}; margin-top: 10px;">
        <div class="metric-label">OPTIMAL TRACK</div>
        <div class="metric-value" style="font-size: 1.5rem;">{best_track}</div>
    </div>
    """, unsafe_allow_html=True)


def render_kpis(data: dict):
    """Renderiza los KPIs principales del piloto"""
    k1, k2, k3 = st.columns(3)

    with k1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TYRE MANAGEMENT</div>
            <div class="metric-value" style="color: #FFD700;">{data.get("tyreManagementIndex", "N/A")}</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">CONSISTENCY SCORE</div>
            <div class="metric-value" style="color: #00F0FF;">{data.get("consistencyScore", "N/A")}</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">WET WEATHER RATING</div>
            <div class="metric-value" style="color: #39FF14;">{data.get("wetWeatherRating", "N/A")}</div>
        </div>
        """, unsafe_allow_html=True)


def render_sector_performance(data: dict):
    """Renderiza el análisis de dominancia por sector"""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h4 style="color: #8b949e; letter-spacing: 2px;">SECTOR DOMINANCE ANALYSIS</h4>', unsafe_allow_html=True)

    sector_data = data.get("sectorPerformanceProfile", {})
    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown(render_sector_box("HIGH SPEED", sector_data.get('high_speed', '-')), unsafe_allow_html=True)
    with s2:
        st.markdown(render_sector_box("MED SPEED", sector_data.get('medium_speed', '-')), unsafe_allow_html=True)
    with s3:
        st.markdown(render_sector_box("LOW SPEED", sector_data.get('low_speed', '-')), unsafe_allow_html=True)


def render_driver_intel_tab():
    """Renderiza el tab completo de inteligencia de pilotos"""
    col_sel, col_content = st.columns([1, 5])

    with col_sel:
        st.markdown("#### SELECT DRIVER")
        selected_driver = st.radio(
            "Driver",
            list(DRIVER_IMAGES.keys()),
            label_visibility="collapsed"
        )
        st.markdown("---")
        if st.button("🔄 SYNC DATA", use_container_width=True):
            st.rerun()

    with col_content:
        try:
            with st.spinner(f"📡 DOWNLINKING TELEMETRY FOR {selected_driver}..."):
                status_code, data = get_driver_data(selected_driver)

            if status_code == 200 and data:
                # Obtener metadatos visuales
                team_name = data.get("team", "Unknown Team")
                team_color = TEAM_COLORS.get(team_name, "#FF1801")
                driver_img = DRIVER_IMAGES.get(selected_driver)

                # Renderizar panel del piloto
                render_driver_panel(data, selected_driver, team_color)

                # Grid de datos
                c_img, c_stats = st.columns([1.5, 3.5])

                with c_img:
                    render_driver_image_and_best_track(
                        driver_img,
                        data.get("bestTrack", "N/A"),
                        team_color
                    )

                with c_stats:
                    render_kpis(data)
                    render_sector_performance(data)
            else:
                st.error(f"❌ TELEMETRY OFFLINE. SERVER CODE: {status_code}")

        except Exception as e:
            st.warning("⚠️ DATA LINK INTERRUPTED")
            st.code(str(e), language="bash")
