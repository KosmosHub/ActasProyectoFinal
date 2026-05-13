from core.excel_parser import agrupar_por_columnas
from core.database import registrar_acta, registrar_productos, guardar_proveedor
from core.pdf_generator import generar_acta
from datetime import datetime

def analizar_excel_previa(ruta_excel):
    datos = agrupar_por_columnas(ruta_excel)
    resumen = []
    for rbd, info in datos.items():
        resumen.append({
            "nombre": f"{info['nombre']} ({rbd})",
            "productos": len(info['productos']),
            "total": info["subtotal"] * 1.19, # IVA incluido
            "rbd": rbd
        })
    return resumen

def procesar_final(ruta_excel, datos_ui):
    datos_colegios = agrupar_por_columnas(ruta_excel)
    if not datos_colegios: return False

    guardar_proveedor(datos_ui['proveedor_nombre'], datos_ui['proveedor_rut'])
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    for rbd, info in datos_colegios.items():
        total_iva = info["subtotal"] * 1.19
        payload = {
            "fecha": fecha_hoy, "rbd": rbd, "establecimiento": info["nombre"],
            "proveedor": datos_ui['proveedor_nombre'], "rut": datos_ui['proveedor_rut'],
            "financiamiento": datos_ui['financiamiento'], "orden_compra": datos_ui['orden_compra'],
            "total": total_iva, "monto_total_formateado": f"{total_iva:,.0f}",
            "factura": "_______", "guia": "_______", "folio_provisorio": "SN",
            "receptor": "_______________", "cargo": "_______________"
        }
        
        ruta_pdf = generar_acta(payload, info["productos"])
        if ruta_pdf:
            payload["ruta_archivo"] = ruta_pdf
            folio = registrar_acta(payload)
            registrar_productos(folio, info["productos"])
    return True