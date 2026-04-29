from core.excel_parser import cargar_excel, detectar_hoja_valida, agrupar_por_filas
from core.pdf_generator import generar_acta
from core.database import (registrar_acta, registrar_productos, 
                           guardar_proveedor, obtener_maestra_colegios)
from datetime import datetime

def analizar_excel_previa(ruta_excel):
    maestra = obtener_maestra_colegios()
    hojas = cargar_excel(ruta_excel)
    if not hojas: return []
    
    df = detectar_hoja_valida(hojas)
    colegios_detectados = agrupar_por_filas(df, maestra)
    
    resumen = []
    for rbd, info in colegios_detectados.items():
        resumen.append({
            "nombre": f"{info['nombre']} ({rbd})",
            "productos": len(info['productos']),
            "total": sum(p["total"] for p in info['productos']),
            "rbd": rbd
        })
    return resumen

def procesar_final(ruta_excel, datos_ui):
    maestra = obtener_maestra_colegios()
    hojas = cargar_excel(ruta_excel)
    df = detectar_hoja_valida(hojas)
    colegios = agrupar_por_filas(df, maestra)
    
    if not colegios: return False

    guardar_proveedor(datos_ui['proveedor_nombre'], datos_ui['proveedor_rut'])
    
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    for rbd, info in colegios.items():
        datos_acta = {
            "fecha_registro": fecha_hoy, "rbd": rbd,
            "financiamiento": datos_ui['financiamiento'],
            "orden_compra": datos_ui['orden_compra'],
            "proveedor_nombre": datos_ui['proveedor_nombre'],
            "proveedor_rut": datos_ui['proveedor_rut'],
            "total": sum(p["total"] for p in info['productos'])
        }
        ruta_pdf = generar_acta(datos_acta, info['productos'])
        if ruta_pdf:
            datos_acta["ruta_archivo"] = ruta_pdf
            folio = registrar_acta(datos_acta)
            registrar_productos(folio, info['productos'])
    return True