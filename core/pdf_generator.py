import os
import re
import pdfkit
from jinja2 import Environment, FileSystemLoader
from config.settings import TEMPLATES_DIR, OUTPUT_DIR, WKHTMLTOPDF_PATH

def limpiar_texto(t):
    return re.sub(r'[<>:"/\\|?*\n\r]', '', str(t)).strip()

def generar_acta(datos, productos):
    try:
        # Opciones para permitir archivos locales (logo) y UTF-8
        options = {
            'enable-local-file-access': None,
            'encoding': "UTF-8",
            'quiet': '',
            'no-stop-slow-scripts': None
        }
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
        
        oc_folder = f"OC_{limpiar_texto(datos['orden_compra'])}"
        ruta_carpeta = os.path.join(OUTPUT_DIR, oc_folder)
        os.makedirs(ruta_carpeta, exist_ok=True)

        nombre_pdf = f"Acta_{limpiar_texto(datos['rbd'])}.pdf"
        ruta_pdf = os.path.join(ruta_carpeta, nombre_pdf)

        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template = env.get_template("acta_template.html")
        
        # Generar el HTML con las variables d y productos
        html_content = template.render(d=datos, productos=productos)

        # Crear el PDF
        pdfkit.from_string(html_content, ruta_pdf, configuration=config, options=options)
        return os.path.join(oc_folder, nombre_pdf)
        
    except Exception as e:
        print(f"Error detallado en PDF para {datos.get('rbd_nombre')}: {e}")
        return None