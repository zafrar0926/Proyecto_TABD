"""
Cliente para interactuar con la API de FastAPI
"""
import requests
from typing import Dict, Optional, Tuple
from config.constants import API_BASE_URL, API_HEALTH_ENDPOINT, API_DRIVER_ENDPOINT


def check_api_status() -> Tuple[bool, Optional[Dict]]:
    """
    Verifica el estado de la API

    Returns:
        Tuple[bool, Optional[Dict]]: (is_online, response_data)
    """
    try:
        response = requests.get(f"{API_BASE_URL}{API_HEALTH_ENDPOINT}", timeout=1)
        return True, response.json()
    except Exception:
        return False, None


def get_driver_data(driver_code: str) -> Tuple[int, Optional[Dict]]:
    """
    Obtiene los datos de un piloto específico

    Args:
        driver_code: Código de 3 letras del piloto (ej: "VER", "HAM")

    Returns:
        Tuple[int, Optional[Dict]]: (status_code, data)
    """
    try:
        response = requests.get(
            f"{API_BASE_URL}{API_DRIVER_ENDPOINT}/{driver_code}",
            timeout=2
        )
        return response.status_code, response.json() if response.status_code == 200 else None
    except Exception as e:
        raise Exception(f"Error fetching driver data: {str(e)}")
