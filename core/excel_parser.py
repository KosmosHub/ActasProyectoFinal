import pandas as pd
import re

def normalizar(texto):
    if not texto: return ""
    t = str(texto).upper()
    # Eliminamos caracteres especiales que ensucian la comparación
    t = re.sub(r'[.\-,\(\)°#]', ' ', t)
    return " ".join(t.split())

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
    
    # Normalizamos los datos de la BD para comparar
    maestra_preparada = []
    for c in maestra_colegios:
        maestra_preparada.append({
            "rbd": normalizar(c['rbd']),
            "nombre": normalizar(c['nombre']),
            "alias": normalizar(c['alias']),
            "original": c['nombre'],
            "rbd_original": c['rbd']
        })

    for _, fila in df.iterrows():
        # Convertimos la fila a un solo bloque de texto limpio
        bloque_fila = normalizar(" ".join([str(v) for v in fila if pd.notna(v)]))
        if not bloque_fila: continue

        # 1. BUSCADOR TRIPLE (RBD, NOMBRE o ALIAS)
        encontrado = False
        for c in maestra_preparada:
            # ¿Aparece el RBD, el Nombre o el Alias en esta fila?
            if (c['rbd'] in bloque_fila or 
                c['nombre'] in bloque_fila or 
                c['alias'] in bloque_fila):
                
                colegio_actual_rbd = c['rbd_original']
                colegio_actual_nombre = c['original']
                
                if colegio_actual_rbd not in grupos:
                    grupos[colegio_actual_rbd] = {
                        "nombre": colegio_actual_nombre,
                        "productos": []
                    }
                encontrado = True
                print(f"✅ Coincidencia hallada: {colegio_actual_nombre} (RBD: {colegio_actual_rbd})")
                break
        
        if encontrado: continue

        # 2. CAPTURA DE PRODUCTOS
        datos_limpios = [str(v).strip() for v in fila if pd.notna(v)]
        if colegio_actual_rbd and len(datos_limpios) >= 3:
            try:
                # El total suele ser el último número de la fila
                ultimo = datos_limpios[-1].replace('$', '').replace('.', '').replace(',', '').strip()
                if ultimo.isdigit() and float(ultimo) > 0:
                    grupos[colegio_actual_rbd]["productos"].append({
                        "producto": datos_limpios[1] if len(datos_limpios) > 1 else datos_limpios[0],
                        "cantidad": datos_limpios[2] if len(datos_limpios) > 2 else "1",
                        "precio_unit": 0,
                        "total": float(ultimo)
                    })
            except:
                continue

    return grupos