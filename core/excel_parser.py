import pandas as pd
import re

def normalizar(texto):
    """Limpia el texto para facilitar la comparación."""
    if not texto: return ""
    t = str(texto).upper()
    t = re.sub(r'[.\-,\(\)°#]', ' ', t) # Quita puntos, guiones y paréntesis
    return " ".join(t.split()) # Quita espacios extra

def cargar_excel(ruta):
    try:
        return pd.read_excel(ruta, sheet_name=None)
    except Exception as e:
        print(f"Error Excel: {e}")
        return None

def detectar_hoja_valida(hojas):
    for _, df in hojas.items():
        if not df.empty: return df
    return None

def agrupar_por_filas(df, maestra_colegios):
    grupos = {}
    colegio_actual_rbd = None
    colegio_actual_nombre = None
    
    # Preparamos los nombres de la BD para comparaciones Regex (flexibles)
    maestra_prep = []
    for c in maestra_colegios:
        # Escapamos los nombres para usarlos en Regex (por si tienen caracteres especiales)
        maestra_prep.append({
            "regex_rbd": re.compile(re.escape(normalizar(c['rbd'])), re.IGNORECASE),
            "regex_nombre": re.compile(re.escape(normalizar(c['nombre'])), re.IGNORECASE),
            "regex_alias": re.compile(re.escape(normalizar(c['alias'])), re.IGNORECASE),
            "original": c['nombre'],
            "rbd_original": c['rbd']
        })

    print("🔎 Iniciando escaneo de Excel...")

    for i, fila in df.iterrows():
        # Unimos toda la fila en un solo bloque de texto limpio
        bloque_fila = normalizar(" ".join([str(v) for v in fila if pd.notna(v)]))
        
        if not bloque_fila: continue

        # 1. BUSCADOR TRIPLE FLEXIBLE (RBD, NOMBRE o ALIAS)
        encontrado_en_fila = False
        for c in maestra_prep:
            # Buscamos coincidencias Regex en la fila completa
            if (c['regex_rbd'].search(bloque_fila) or 
                c['regex_nombre'].search(bloque_fila) or 
                c['regex_alias'].search(bloque_fila)):
                
                colegio_actual_rbd = c['rbd_original']
                colegio_actual_nombre = c['original']
                
                if colegio_actual_rbd not in grupos:
                    grupos[colegio_actual_rbd] = {
                        "nombre": colegio_actual_nombre,
                        "productos": []
                    }
                encontrado_en_fila = True
                print(f"✅ MATCH hallado en fila {i+1}: {colegio_actual_nombre} ({colegio_actual_rbd})")
                break
        
        if encontrado_en_fila: continue

        # 2. CAPTURA DE PRODUCTOS
        datos_limpios = [str(v).strip() for v in fila if pd.notna(v)]
        if colegio_actual_rbd and len(datos_limpios) >= 3:
            try:
                # El total suele ser el último número de la fila
                ultimo = datos_limpios[-1].replace('$', '').replace('.', '').replace(',', '').strip()
                
                # 🔹 FILTRO ANTIBASURA:
                # Verificamos que sea número, que el producto no sea numérico (evita subtotales)
                # y que la descripción sea larga.
                descripcion_producto = datos_limpios[1] if len(datos_limpios) > 1 else datos_limpios[0]
                
                es_monto_valido = ultimo.replace('.','').isdigit() and float(ultimo.replace('.','')) > 0
                es_desc_valida = not descripcion_producto.replace('.','').isdigit() and len(descripcion_producto) > 5

                if es_monto_valido and es_desc_valida:
                    # Ajustamos captura (Cant, Desc, Total)
                    grupos[colegio_actual_rbd]["productos"].append({
                        "producto": descripcion_producto,
                        "cantidad": datos_limpios[2] if len(datos_limpios) > 2 else "1 Unid.",
                        "precio_unit": 0, # Calculado opcionalmente
                        "total": float(ultimo.replace('.',''))
                    })
            except Exception as e:
                continue

    # Devolvemos solo colegios con productos reales detectados
    resultado = {k: v for k, v in grupos.items() if len(v) > 0}
    print(f"📊 Resumen Escaneo: Se detectaron {len(resultado)} establecimientos con productos.")
    return resultado