import os
import re
import pdfkit
from jinja2 import Environment, FileSystemLoader
from config.settings import TEMPLATES_DIR, OUTPUT_DIR, WKHTMLTOPDF_PATH

def limpiar_texto(t):
    return re.sub(r'[<>:"/\\|?*\n\r]', '', str(t)).strip()

def generar_acta(datos, productos):
    try:
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
        oc_folder = f"OC_{limpiar_texto(datos['orden_compra'])}"
        ruta_carpeta = os.path.join(OUTPUT_DIR, oc_folder)
        os.makedirs(ruta_carpeta, exist_ok=True)

        nombre_pdf = f"Acta_{limpiar_texto(datos['rbd'])}.pdf"
        ruta_pdf = os.path.join(ruta_carpeta, nombre_pdf)

        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template = env.get_template("acta_template.html")
        html_content = template.render(d=datos, productos=productos)

        pdfkit.from_string(html_content, ruta_pdf, configuration=config)
        return os.path.join(oc_folder, nombre_pdf)
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        return None