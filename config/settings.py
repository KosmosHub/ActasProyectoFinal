import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuración de Base de Datos
DATABASE_PATH = os.path.join(BASE_DIR, "data", "BD_ActasDespacho.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMPLATES_DIR = os.path.join(OUTPUT_DIR, "templates")

# RUTA DEL MOTOR PDF (Ajusta si lo instalaste en otra carpeta)
WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'