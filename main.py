from core.excel_parser import agrupar_por_columnas
from core.database import registrar_acta, registrar_productos, guardar_proveedor
from core.pdf_generator import generar_acta
from datetime import datetime

def analizar_excel_previa(ruta_excel):
    """Genera el resumen para la vista previa del UI."""
    datos = agrupar_por_columnas(ruta_excel)
    resumen = []
    for rbd, info in datos.items():
        resumen.append({
            "nombre": f"{info['nombre']} ({rbd})",
            "productos": len(info['productos']),
            "total": info["subtotal"] * 1.19,
            "rbd": rbd
        })
    return resumen

def procesar_final(ruta_excel, datos_ui):
    """Genera los PDFs calculando Neto, IVA y Total para el frontend."""
    datos_colegios = agrupar_por_columnas(ruta_excel)
    if not datos_colegios: return False

    guardar_proveedor(datos_ui['proveedor_nombre'], datos_ui['proveedor_rut'])
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    for rbd, info in datos_colegios.items():
        # Cálculos de Backend
        neto = info["subtotal"]
        iva = neto * 0.19
        total = neto + iva

        payload = {
            "fecha": fecha_hoy,  # Se mantiene en el payload para la DB, pero no se imprime en el texto según orden
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
            # Nuevos campos formateados para la tabla de totales
            "neto_formateado": f"{neto:,.0f}",
            "iva_formateado": f"{iva:,.0f}",
            "total_formateado": f"{total:,.0f}"
        }
        
        # El campo 'total' ya viene calculado en productos[].total dentro de info['productos']
        ruta_pdf = generar_acta(payload, info["productos"])
        
        if ruta_pdf:
            payload["ruta_archivo"] = ruta_pdf
            payload["total"] = total
            folio = registrar_acta(payload)
            registrar_productos(folio, info["productos"])
            
    return True