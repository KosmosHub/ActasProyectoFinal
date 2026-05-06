from core.excel_parser import cargar_excel, detectar_hoja_valida, agrupar_por_filas
from core.pdf_generator import generar_acta
from core.database import (registrar_acta, registrar_productos, 
                           guardar_proveedor, obtener_maestra_colegios)
from datetime import datetime

def analizar_excel_previa(ruta_excel):
    # Cargamos RBD, Nombres y Alias de SQLite
    maestra = obtener_maestra_colegios()
    
    hojas = cargar_excel(ruta_excel)
    if not hojas: return []
    
    df = detectar_hoja_valida(hojas)
    # Buscamos coincidencias triples y flexibles
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
    # Volvemos a leer la BD y el Excel para el proceso real
    maestra = obtener_maestra_colegios()
    hojas = cargar_excel(ruta_excel)
    df = detectar_hoja_valida(hojas)
    colegios = agrupar_por_filas(df, maestra)
    
    if not colegios: 
        print("❌ No hay colegios válidos detectados para procesar.")
        return False

    # Guardar proveedor en memoria
    guardar_proveedor(datos_ui['proveedor_nombre'], datos_ui['proveedor_rut'])
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    print(f"🚀 Iniciando generación de {len(colegios)} actas PDF...")

    for rbd, info in colegios.items():
        monto_total = sum(p["total"] for p in info['productos'])
        
        # 🔹 SINCRONIZACIÓN DE ETIQUETAS CON EL HTML
        datos_acta = {
            "fecha": fecha_hoy, 
            "rbd": rbd,
            "establecimiento": info['nombre'],
            "financiamiento": datos_ui['financiamiento'],
            "orden_compra": datos_ui['orden_compra'],
            "proveedor": datos_ui['proveedor_nombre'],
            "rut": datos_ui['proveedor_rut'],
            "monto_total_formateado": f"{monto_total:,.0f}", # Formato chileno
            "receptor": "_______________", # Espacio manual en el PDF
            "cargo": "_______________", # Espacio manual en el PDF
            "factura": "_______________", # Espacio manual en el PDF
            "guia": "_______________" # Espacio manual en el PDF
        }
        
        # Generar PDF y obtener ruta para la BD
        ruta_pdf = generar_acta(datos_acta, info['productos'])
        
        if ruta_pdf:
            datos_acta["ruta_archivo"] = ruta_pdf
            # Guardamos el total numérico real en la BD actas
            datos_acta["total"] = monto_total 
            folio = registrar_acta(datos_acta)
            registrar_productos(folio, info['productos'])
            print(f"✅ Acta generada y guardada para: {info['nombre']}")
    return True