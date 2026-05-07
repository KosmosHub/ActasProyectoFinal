from core.excel_parser import cargar_excel, detectar_hoja_valida, agrupar_por_columnas
from core.pdf_generator import generar_acta
from core.database import (
    registrar_acta,
    registrar_productos,
    guardar_proveedor,
    obtener_maestra_colegios
)
from datetime import datetime

def analizar_excel_previa(ruta_excel):
    """Analiza el Excel y devuelve un resumen por colegio detectado."""
    maestra = obtener_maestra_colegios()
    hojas = cargar_excel(ruta_excel)
    if not hojas:
        return []

    df = detectar_hoja_valida(hojas)
    colegios_detectados = agrupar_por_columnas(df, maestra)

    resumen = []
    for rbd, info in colegios_detectados.items():
        resumen.append({
            "nombre": f"{info['nombre']} ({rbd})",
            "productos": len(info['productos']),
            "subtotal": info["subtotal"],
            "iva": info["iva"],
            "total_con_iva": info["total_con_iva"],
            "rbd": rbd
        })
    return resumen

def procesar_final(ruta_excel, datos_ui):
    """Procesa el Excel y genera actas PDF por cada colegio detectado."""
    maestra = obtener_maestra_colegios()
    hojas = cargar_excel(ruta_excel)
    df = detectar_hoja_valida(hojas)
    colegios = agrupar_por_columnas(df, maestra)

    if not colegios:
        print("❌ No se detectaron colegios válidos para procesar.")
        return False

    guardar_proveedor(datos_ui['proveedor_nombre'], datos_ui['proveedor_rut'])
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    print(f"🚀 Iniciando generación de {len(colegios)} actas PDF...")

    for rbd, info in colegios.items():
        datos_acta = {
            "fecha": fecha_hoy,
            "rbd": rbd,
            "establecimiento": info['nombre'],
            "financiamiento": datos_ui['financiamiento'],
            "orden_compra": datos_ui['orden_compra'],
            "proveedor": datos_ui['proveedor_nombre'],
            "rut": datos_ui['proveedor_rut'],
            "monto_total_formateado": f"{info['total_con_iva']:,.0f}",
            "receptor": "_______________",
            "cargo": "_______________",
            "factura": "_______________",
            "guia": "_______________",
            "folio_provisorio": "SN"
        }

        ruta_pdf = generar_acta(datos_acta, info['productos'])

        if ruta_pdf:
            datos_acta["ruta_archivo"] = ruta_pdf
            datos_acta["total"] = info["total_con_iva"]
            folio = registrar_acta(datos_acta)
            registrar_productos(folio, info['productos'])
            print(f"✅ Acta generada y guardada para: {info['nombre']}")

    return True
