"""
Módulo de Configuración
=======================

Carga las variables de entorno desde el archivo .env
y las expone como constantes globales para toda la aplicación.

Uso:
    from src.config import DB_HOST, DB_USER, DB_PASSWORD

Requiere:
    - python-dotenv (instalar con: pip install python-dotenv)
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# Ruta al archivo .env (ubicado en la raíz del proyecto)
BASE_DIR = Path(__file__).parent.parent
ENV_PATH = BASE_DIR / ".env"

# Cargar variables de entorno desde .env
load_dotenv(ENV_PATH)


# ---------------------------------------------------
# Configuración de Base de Datos
# ---------------------------------------------------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "empleados_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


# ---------------------------------------------------
# Configuración de Seguridad
# ---------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-change-me")
BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", 12))
MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", 5))
BLOCK_TIME_MINUTES = int(os.getenv("BLOCK_TIME_MINUTES", 15))
SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", 30))


# ---------------------------------------------------
# Función para obtener string de conexión
# ---------------------------------------------------
def get_connection_string():
    """
    Genera el string de conexión para MariaDB.
    
    Returns:
        str: String de conexión formateado
    """
    return f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_mysql_connection_params():
    """
    Obtiene los parámetros de conexión como diccionario.
    
    Returns:
        dict: Parámetros de conexión para mysql-connector
    """
    return {
        "host": DB_HOST,
        "port": DB_PORT,
        "database": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD
    }
