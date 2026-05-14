import pandas as pd
import re
import difflib
from core.database import obtener_maestra_colegios

def limpiar_texto(t):
    return re.sub(r'[^A-Z0-9]', '', str(t).upper()) if t else ""

def agrupar_por_columnas(ruta_excel):
    maestra = obtener_maestra_colegios()
    if not maestra: return {}

    try:
        # Cargamos el Excel sin encabezados para mapear libremente
        df = pd.read_excel(ruta_excel, header=None)
        resultados = {}

        # Localizar el ancla "PRODUCTOS SOLICITADOS"
        fila_encabezados = 0
        col_prod, col_precio = None, None

        for r in range(min(30, len(df))): # Escaneo extendido a 30 filas
            fila_str = df.iloc[r].astype(str).str.upper()
            if fila_str.str.contains("PRODUCTOS SOLICITADOS").any():
                fila_encabezados = r
                col_prod = fila_str.str.contains("PRODUCTOS SOLICITADOS").idxmax()
                break
        
        if col_prod is None: return {}

        # Localizar columna de PRECIO
        fila_headers = df.iloc[fila_encabezados].astype(str).str.upper()
        if fila_headers.str.contains("PRECIO").any():
            col_precio = fila_headers.str.contains("PRECIO").idxmax()

        # Identificar columnas de colegios
        for c in range(len(df.columns)):
            val_celda = str(df.iloc[fila_encabezados, c]).upper()
            if any(x in val_celda for x in ["ITEM", "PRODUCTO", "UNIDAD", "CANTIDAD", "PRECIO", "TOTAL", "NAN"]):
                continue

            for m in maestra:
                nom_db = limpiar_texto(m['nombre'])
                alias_db = limpiar_texto(m.get('alias', ''))
                val_excel = limpiar_texto(val_celda)

                # Si el encabezado del Excel es parte del nombre en la DB (o viceversa)
                if val_excel and (val_excel in nom_db or nom_db in val_excel or (alias_db and alias_db in val_excel)):
                    rbd = m['rbd']
                    productos_colegio = []
                    sub_acumulado = 0

                    for r in range(fila_encabezados + 1, len(df)):
                        desc = str(df.iloc[r, col_prod]).strip()
                        cant = df.iloc[r, c]
                        
                        if desc and desc != "nan":
                            try:
                                val_cant = float(cant)
                                if val_cant > 0:
                                    p_raw = str(df.iloc[r, col_precio] if col_precio is not None else 0)
                                    p_val = float(re.sub(r'[^\d.]', '', p_raw.replace(',', '.')))
                                    
                                    productos_colegio.append({
                                        "producto": desc,
                                        "cantidad": int(val_cant),
                                        "precio_unit": p_val,
                                        "total": val_cant * p_val
                                    })
                                    sub_acumulado += (val_cant * p_val)
                            except: continue

                    if productos_colegio:
                        resultados[rbd] = {
                            "nombre": m['nombre'],
                            "productos": productos_colegio,
                            "subtotal": sub_acumulado
                        }
                    break
        return resultados
    except Exception as e:
        print(f"Error: {e}")
        return {}