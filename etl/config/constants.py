"""
Constantes de configuración para la aplicación F1 Mission Control
"""

# URLs de imágenes de pilotos
DRIVER_IMAGES = {
    "VER": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/2col/image.png",
    "HAM": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/L/LEWHAM01_Lewis_Hamilton/lewham01.png.transform/2col/image.png",
    "NOR": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.png.transform/2col/image.png",
    "LEC": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/C/CHALEC01_Charles_Leclerc/chalec01.png.transform/2col/image.png",
    "SAI": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/C/CARSAI01_Carlos_Sainz/carsai01.png.transform/2col/image.png",
    "PIA": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/O/OSCPIA01_Oscar_Piastri/oscpia01.png.transform/2col/image.png",
    "ALO": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/F/FERALO01_Fernando_Alonso/feralo01.png.transform/2col/image.png",
    "STR": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/L/LANSTR01_Lance_Stroll/lanstr01.png.transform/2col/image.png",
    "RUS": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/G/GEORUS01_George_Russell/georus01.png.transform/2col/image.png",
    "GAS": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/P/PIEGAS01_Pierre_Gasly/piegas01.png.transform/2col/image.png",
    "OCO": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/E/ESTOCO01_Esteban_Ocon/estoco01.png.transform/2col/image.png",
    "ALB": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/A/ALEALB01_Alexander_Albon/alealb01.png.transform/2col/image.png"
}

# Colores de equipos
TEAM_COLORS = {
    "Red Bull Racing": "#1E41FF",
    "Mercedes": "#00D2BE",
    "Ferrari": "#DC0000",
    "McLaren": "#FF8700",
    "Aston Martin": "#006F62",
    "Alpine": "#0090FF",
    "Williams": "#005AFF",
    "Haas F1 Team": "#B6BABD",
    "Kick Sauber": "#52E252",
    "RB": "#6692FF"
}

# URLs de API
API_BASE_URL = "http://127.0.0.1:8000"
API_HEALTH_ENDPOINT = "/"
API_DRIVER_ENDPOINT = "/driver"

# URLs de Looker Studio
DEFAULT_LOOKER_URL = "https://lookerstudio.google.com/embed/reporting/14b2dcfe-5a7e-49b2-8ecf-6f2e22d6051a/page/p_ealwatq5xd"

# Configuración de ETL
INGESTA_YEAR = 2025
ETL_SLEEP_INTERVAL = 30  # segundos entre ciclos de ingesta

# URLs de recursos externos
F1_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg"
