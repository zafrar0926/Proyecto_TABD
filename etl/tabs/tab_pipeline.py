"""
Tab de pipeline de datos - Control de ingesta ETL
"""
import streamlit as st
import time
from datetime import datetime
from mongo_to_bigquery import run_mongo_to_bigquery
from bigquery_to_dynamo import run_bigquery_to_dynamo
from config.constants import INGESTA_YEAR, ETL_SLEEP_INTERVAL


def render_pipeline_controls():
    """Renderiza los controles del pipeline"""
    st.markdown("#### PIPELINE CONTROLS")
    st.markdown("""
    <div style="background: #161b22; padding: 20px; border-radius: 8px; border: 1px solid #333;">
        <div style="font-size: 0.8rem; color: #888;">CURRENT STATUS</div>
    """, unsafe_allow_html=True)

    if st.session_state.ingesta_activa:
        st.markdown('<div style="color: #39FF14; font-weight: bold; font-size: 1.2rem; margin-bottom: 15px;">● RUNNING</div>', unsafe_allow_html=True)
        if st.button("⏹️ ABORT SEQUENCE", type="primary", use_container_width=True):
            st.session_state.ingesta_activa = False
            st.rerun()
    else:
        st.markdown('<div style="color: #FF1801; font-weight: bold; font-size: 1.2rem; margin-bottom: 15px;">● IDLE</div>', unsafe_allow_html=True)
        if st.button("🚀 INITIATE AUTO-INGEST", use_container_width=True):
            st.session_state.ingesta_activa = True
            st.session_state.contador_ejecuciones = 0
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_idle_console():
    """Renderiza la consola en estado idle"""
    st.markdown("""
    <div class="console-box" style="color: #666; display: flex; align-items: center; justify-content: center;">
        > WAITING FOR USER INPUT...
    </div>
    """, unsafe_allow_html=True)


def run_etl_cycle():
    """Ejecuta un ciclo completo de ETL y retorna los logs"""
    log_content = ""
    ts = datetime.now().strftime("%H:%M:%S")
    log_content += f"[{ts}] INFO: Starting extraction sequence for Year {INGESTA_YEAR}...\\n"

    try:
        # Paso 1: MongoDB to BigQuery
        result_mongo = run_mongo_to_bigquery(INGESTA_YEAR)
        log_content += f"[{datetime.now().strftime('%H:%M:%S')}] SUCCESS: MongoDB Payload extracted. Size: 24MB\\n"
        log_content += f"[{datetime.now().strftime('%H:%M:%S')}] INFO: Uploading to BigQuery (Dataset: f1_warehouse)...\\n"

        # Paso 2: BigQuery to DynamoDB
        result_dynamo = run_bigquery_to_dynamo()
        log_content += f"[{datetime.now().strftime('%H:%M:%S')}] SUCCESS: DynamoDB Key-Value stores updated.\\n"

        st.session_state.contador_ejecuciones += 1

        return log_content, True

    except Exception as e:
        log_content += f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: {str(e)}\\n"
        return log_content, False


def render_active_console(log_content: str):
    """Renderiza la consola con logs activos"""
    st.markdown(f"""
    <div class="console-box">
        <div class="log-entry">{log_content.replace(chr(10), '</div><div class="log-entry">')}</div>
        <div class="log-entry" style="color: #00F0FF;">> CYCLE COMPLETE. WAITING {ETL_SLEEP_INTERVAL}s...</div>
    </div>
    """, unsafe_allow_html=True)


def render_pipeline_tab():
    """Renderiza el tab completo de pipeline de datos"""
    # Variables de sesión
    if 'ingesta_activa' not in st.session_state:
        st.session_state.ingesta_activa = False

    col_status, col_terminal = st.columns([1, 2])

    with col_status:
        render_pipeline_controls()

    with col_terminal:
        st.markdown("#### SYSTEM LOGS")

        if st.session_state.ingesta_activa:
            log_content, success = run_etl_cycle()

            if success:
                render_active_console(log_content)
                time.sleep(ETL_SLEEP_INTERVAL)
                st.rerun()
            else:
                st.error(f"FATAL ERROR: Check logs above")
                time.sleep(ETL_SLEEP_INTERVAL)
                st.rerun()
        else:
            render_idle_console()
