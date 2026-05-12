import os
import sys

# Determina la raíz del proyecto de forma absoluta
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuración de Base de Datos
DATABASE_PATH = os.path.join(BASE_DIR, "data", "BD_ActasDespacho.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMPLATES_DIR = os.path.join(OUTPUT_DIR, "templates")

# Crear carpetas si no existen para evitar errores de E/S
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# RUTA DEL MOTOR PDF (Ajustada a ruta estándar de Windows)
WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
LOGS_PATH = os.path.join(BASE_DIR, "core", "logs.log")