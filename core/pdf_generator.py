from jinja2 import Environment, FileSystemLoader
import pdfkit
import os

TEMPLATES_DIR = "output/templates"
OUTPUT_DIR = "output"

def generar_acta(datos, productos):
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("acta_template.html")

    html_renderizado = template.render(
        fecha=datos["fecha"],
        receptor=datos["receptor"],
        cargo=datos["cargo"],
        establecimiento=datos["nrc"],
        financiamiento=datos["financiamiento"],
        orden_compra=datos["orden_compra"],
        factura=datos["factura"],
        guia=datos["guia"],
        proveedor=datos["proveedor"],
        rut=datos["rut"],
        productos=productos,
        total=datos["total"]
    )

    ruta_html = os.path.join(OUTPUT_DIR, f"acta_{datos['nrc']}.html")
    ruta_pdf = os.path.join(OUTPUT_DIR, f"acta_{datos['nrc']}.pdf")

    with open(ruta_html, "w", encoding="utf-8") as f:
        f.write(html_renderizado)

    pdfkit.from_file(ruta_html, ruta_pdf)
    return ruta_pdf
