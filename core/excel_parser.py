import pandas as pd
import re
from core.database import obtener_maestra_colegios

def limpiar_texto(t):
    return re.sub(r'[^A-Z0-9]', '', str(t).upper()) if t else ""

def agrupar_por_columnas(ruta_excel):
    maestra = obtener_maestra_colegios()
    if not maestra: return {}

    try:
        # Cargamos el Excel sin encabezados para buscar la posición real de los datos
        df = pd.read_excel(ruta_excel, header=None)
        resultados = {}

        # 1. Localizar coordenadas de la tabla
        fila_encabezados = 0
        col_prod, col_precio = None, None

        for r in range(min(20, len(df))):
            fila_str = df.iloc[r].astype(str).str.upper()
            if fila_str.str.contains("PRODUCTOS SOLICITADOS").any():
                fila_encabezados = r
                col_prod = fila_str.str.contains("PRODUCTOS SOLICITADOS").idxmax()
                break
        
        if col_prod is None: return {}

        # Buscar la columna de PRECIO unitario en la misma fila de encabezados
        fila_headers = df.iloc[fila_encabezados].astype(str).str.upper()
        if fila_headers.str.contains("PRECIO").any():
            col_precio = fila_headers.str.contains("PRECIO").idxmax()

        # 2. Identificar columnas de colegios (basado en coincidencia con la DB)
        for c in range(len(df.columns)):
            val_col = str(df.iloc[fila_encabezados, c]).upper()
            # Ignorar columnas técnicas
            if any(x in val_col for x in ["ITEM", "PRODUCTO", "UNIDAD", "CANTIDAD", "PRECIO", "TOTAL", "IMAGEN"]):
                continue

            for m in maestra:
                nom_db = limpiar_texto(m['nombre'])
                alias_db = limpiar_texto(m.get('alias', ''))
                val_limpio = limpiar_texto(val_col)

                # Si el encabezado contiene al menos un 30% del nombre o el alias
                if (val_limpio and val_limpio in nom_db) or (alias_db and alias_db in val_limpio):
                    rbd = m['rbd']
                    if rbd not in resultados:
                        resultados[rbd] = {"nombre": m['nombre'], "productos": [], "subtotal": 0}

                    # Extraer productos bajo esta columna
                    for r in range(fila_encabezados + 1, len(df)):
                        producto = str(df.iloc[r, col_prod]).strip()
                        cantidad = df.iloc[r, c]
                        
                        if producto and producto != "nan" and not str(cantidad).strip() in ["", "nan", "-", "0"]:
                            try:
                                cant_val = float(cantidad)
                                if cant_val > 0:
                                    p_raw = str(df.iloc[r, col_precio] if col_precio is not None else 0)
                                    p_val = float(re.sub(r'[^\d.]', '', p_raw.replace(',', '.')))
                                    
                                    item = {
                                        "producto": producto,
                                        "cantidad": int(cant_val),
                                        "precio_unit": p_val,
                                        "total": cant_val * p_val
                                    }
                                    resultados[rbd]["productos"].append(item)
                                    resultados[rbd]["subtotal"] += item["total"]
                            except: continue
                    break # Colegio encontrado para esta columna

        return {k: v for k, v in resultados.items() if v["productos"]}
    except Exception as e:
        print(f"❌ Error crítico en escaneo: {e}")
        return {}