"""
Estilos CSS personalizados para la aplicación F1 Mission Control
"""

def get_custom_css():
    """Retorna el CSS personalizado para la aplicación"""
    return """
    <style>
    /* IMPORTAR FUENTES TÉCNICAS */
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Titillium+Web:wght@300;400;600;700&display=swap');

    /* VARIABLES DE COLOR */
    :root {
        --f1-red: #FF1801;
        --tech-cyan: #00F0FF;
        --data-green: #39FF14;
        --dark-bg: #0E1117;
        --card-bg: rgba(22, 27, 34, 0.85);
        --border-color: rgba(255, 255, 255, 0.1);
    }

    /* GLOBAL STYLES */
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(circle at 50% 0%, #1a1a1a 0%, #000000 70%);
    }

    html, body, [class*="css"] {
        font-family: 'Titillium Web', sans-serif;
    }

    /* CABECERA PRINCIPAL */
    .main-header-container {
        border-bottom: 2px solid var(--f1-red);
        padding-bottom: 20px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: end;
    }

    .main-title {
        font-family: 'Michroma', sans-serif; /* Fuente futurista ancha */
        font-size: 3.5rem;
        color: #FFF;
        text-transform: uppercase;
        letter-spacing: -2px;
        margin: 0;
        text-shadow: 0 0 20px rgba(255, 24, 1, 0.4);
    }

    .main-subtitle {
        font-family: 'Titillium Web', sans-serif;
        color: var(--tech-cyan);
        font-size: 1rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    /* TARJETAS DE MÉTRICAS (GLASSMORPHISM) */
    .metric-card {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-color);
        border-top: 3px solid var(--f1-red); /* Default accent */
        border-radius: 4px; /* Bordes más rectos, más técnicos */
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        border-top-color: var(--tech-cyan);
    }

    .metric-label {
        font-size: 0.75rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }

    .metric-value {
        font-family: 'Michroma', sans-serif;
        font-size: 2rem;
        color: #FFF;
    }

    /* PANEL DE PILOTO */
    .driver-panel {
        background: linear-gradient(90deg, rgba(20,20,20,0.9) 0%, rgba(30,30,30,0.6) 100%);
        border-left: 6px solid #FFF; /* Se sobreescribe dinámicamente */
        padding: 30px;
        margin-bottom: 20px;
        border-radius: 0 15px 15px 0;
        position: relative;
    }

    .driver-name {
        font-family: 'Michroma', sans-serif;
        font-size: 4rem;
        line-height: 1;
        color: #FFF;
        margin: 0;
    }

    .team-name {
        font-size: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 4px;
        opacity: 0.8;
    }

    /* PESTAÑAS PERSONALIZADAS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 4px;
        color: #8b949e;
        font-family: 'Titillium Web', sans-serif;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 0 20px;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--f1-red) !important;
        color: #FFF !important;
        border-color: var(--f1-red) !important;
        box-shadow: 0 0 15px rgba(255, 24, 1, 0.4);
    }

    /* CONSOLA DE LOGS */
    .console-box {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: var(--data-green);
        font-size: 0.85rem;
        height: 300px;
        overflow-y: auto;
    }

    .log-entry {
        margin-bottom: 5px;
        border-bottom: 1px solid #21262d;
        padding-bottom: 2px;
    }

    /* SCROLLBAR PERSONALIZADO */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0d1117;
    }
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--f1-red);
    }
    </style>
    """
