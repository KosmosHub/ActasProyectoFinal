from core.excel_parser import agrupar_por_columnas
from core.database import registrar_acta, registrar_productos, guardar_proveedor
from core.pdf_generator import generar_acta
from datetime import datetime

def analizar_excel_previa(ruta_excel):
    datos = agrupar_por_columnas(ruta_excel)
    return [{"nombre": f"{v['nombre']} ({k})", "productos": len(v['productos']), "total": v["subtotal"] * 1.19, "rbd": k} for k, v in datos.items()]

def procesar_final(ruta_excel, datos_ui):
    datos_colegios = agrupar_por_columnas(ruta_excel)
    if not datos_colegios: return False

    guardar_proveedor(datos_ui['proveedor_nombre'], datos_ui['proveedor_rut'])
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    for rbd, info in datos_colegios.items():
        neto = info["subtotal"]
        iva = neto * 0.19
        total = neto + iva

        payload = {
            "fecha": fecha_hoy,
            "rbd": rbd,
            "establecimiento": info["nombre"],
            "proveedor": datos_ui['proveedor_nombre'],
            "rut": datos_ui['proveedor_rut'],
            "financiamiento": datos_ui['financiamiento'],
            "orden_compra": datos_ui['orden_compra'],
            "factura": "_______",
            "guia": "_______",
            "folio_provisorio": "SN",
            "receptor": datos_ui.get('receptor', '_______________'),
            "cargo": datos_ui.get('cargo', '_______________'),
            "neto_formateado": f"{neto:,.0f}",
            "iva_formateado": f"{iva:,.0f}",
            "total_formateado": f"{total:,.0f}"
        }
        
        generar_acta(payload, info["productos"])
    return True