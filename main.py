from core.excel_parser import cargar_excel, detectar_hoja_valida, agrupar_por_filas
from core.pdf_generator import generar_acta
from core.database import registrar_acta, registrar_productos

def procesar_excel(ruta_excel):
    hojas = cargar_excel(ruta_excel)
    if hojas is None:
        raise Exception("No se pudo abrir el archivo Excel.")

    df = detectar_hoja_valida(hojas)
    if df is None:
        raise Exception("No se encontró hoja válida en el Excel.")

    colegios = agrupar_por_filas(df)
    resultados = []

    for nombre_colegio, productos in colegios.items():
        datos = {
            "fecha": "2026-04-20",
            "nrc": nombre_colegio,
            "receptor": "Receptor DEM",
            "cargo": "Encargado",
            "financiamiento": "Subvención Escolar",
            "orden_compra": "",
            "factura": "",
            "guia": "",
            "proveedor": "MUEBLES ANDROMEDA DOS SPA",
            "rut": "",
            "total": sum(p["total"] for p in productos)
        }

        ruta_pdf = generar_acta(datos, productos)
        folio = registrar_acta(datos, ruta_pdf)
        registrar_productos(folio, productos)

        resultados.append(f"Acta {nombre_colegio} → Folio {folio}, PDF: {ruta_pdf}")

    return resultados
