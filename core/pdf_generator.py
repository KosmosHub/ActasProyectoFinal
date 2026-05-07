import os
import pdfkit
from jinja2 import Environment, FileSystemLoader
from config.settings import TEMPLATES_DIR, OUTPUT_DIR, WKHTMLTOPDF_PATH

def generar_acta(datos, productos):
    """
    Genera el PDF inyectando los datos en la plantilla. 
    Mapea 'datos' a 'd' para que coincida con el HTML.
    """
    try:
        options = {
            'enable-local-file-access': None,
            'encoding': "UTF-8",
            'quiet': '',
            'no-stop-slow-scripts': None,
            'page-size': 'Letter',
            'margin-top': '15mm',
            'margin-right': '15mm',
            'margin-bottom': '15mm',
            'margin-left': '15mm'
        }

        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

        oc_limpia = str(datos.get('orden_compra', 'SN')).replace('/', '-').replace('\\', '-')
        oc_folder = f"OC_{oc_limpia}"
        ruta_carpeta = os.path.join(OUTPUT_DIR, oc_folder)
        os.makedirs(ruta_carpeta, exist_ok=True)

        rbd_limpio = str(datos.get('rbd', '0')).strip()
        nombre_pdf = f"Acta_{rbd_limpio}.pdf"
        ruta_pdf = os.path.join(ruta_carpeta, nombre_pdf)

        env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template = env.get_template("acta_template.html")
        
        html_content = template.render(d=datos, productos=productos)

        pdfkit.from_string(html_content, ruta_pdf, configuration=config, options=options)

        print(f"✅ PDF generado en: {ruta_pdf}")

        return os.path.join(oc_folder, nombre_pdf)
        
    except Exception as e:
        import traceback
        print(f"❌ Error en PDF para {datos.get('establecimiento')}: {e}")
        print(traceback.format_exc())
        return None
