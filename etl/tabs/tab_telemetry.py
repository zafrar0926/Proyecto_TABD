"""
Tab de telemetría en vivo - Dashboard de Looker Studio
"""
import streamlit as st
from config.constants import DEFAULT_LOOKER_URL


def render_telemetry_tab():
    """Renderiza el tab de telemetría con el dashboard de Looker Studio"""
    st.markdown('<h3 style="color: #fff; margin-bottom: 15px;">STRATEGIC OVERVIEW</h3>', unsafe_allow_html=True)

    looker_url = st.text_input(
        "Looker Embed URL",
        DEFAULT_LOOKER_URL,
        label_visibility="collapsed"
    )

    # Frame de Looker con efecto de borde neón
    st.markdown("""
    <div style="border: 1px solid #333; border-top: 2px solid #00F0FF; border-radius: 8px; overflow: hidden; box-shadow: 0 0 30px rgba(0, 240, 255, 0.05); background: #000;">
    """, unsafe_allow_html=True)

    st.components.v1.html(
        f"""<iframe src="{looker_url}" width="100%" height="900" frameborder="0" allowfullscreen style="background: #0E1117;"></iframe>""",
        height=900,
    )

    st.markdown("</div>", unsafe_allow_html=True)
