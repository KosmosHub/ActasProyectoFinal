import pandas as pd
import re
import difflib
from core.database import obtener_maestra_colegios

def limpiar(t):
    return re.sub(r'[^A-Z0-9]', '', str(t).upper()) if t else ""

def agrupar_por_columnas(ruta_excel):
    maestra = obtener_maestra_colegios()
    if not maestra: return {}
    
    try:
        # Cargamos el Excel sin encabezados para buscar manualmente la fila de colegios
        df = pd.read_excel(ruta_excel, header=None)
        resultados = {}

        # 1. Identificar columnas de productos y precios (escaneo vertical de las primeras 15 filas)
        col_prod, col_precio, fila_inicio = None, None, 0
        for r in range(min(15, len(df))):
            fila = df.iloc[r].astype(str).str.upper()
            if fila.str.contains("PRODUCTO|DESCRIPCIÓN").any():
                col_prod = fila.str.contains("PRODUCTO|DESCRIPCIÓN").idxmax()
                fila_inicio = r + 1
            if fila.str.contains("PRECIO").any():
                col_precio = fila.str.contains("PRECIO").idxmax()

        if col_prod is None: return {}

        # 2. Buscar colegios en TODA la matriz de las primeras 10 filas
        for c in range(len(df.columns)):
            for r in range(10):
                valor_celda = str(df.iloc[r, c]).upper()
                if any(x in valor_celda for x in ["ITEM", "PRODUCTO", "TOTAL", "UNIDAD", "CANTIDAD"]): continue
                
                for m in maestra:
                    # Match difuso: si el nombre de la DB está contenido en la celda o viceversa
                    if limpiar(m['nombre']) in limpiar(valor_celda) or limpiar(valor_celda) in limpiar(m['nombre']) or (m['alias'] and limpiar(m['alias']) in limpiar(valor_celda)):
                        rbd = m['rbd']
                        if rbd not in resultados:
                            resultados[rbd] = {"nombre": m['nombre'], "productos": [], "subtotal": 0}
                        
                        # Extraer productos bajo esta columna específica
                        for i in range(fila_inicio, len(df)):
                            producto = str(df.iloc[i, col_prod]).strip()
                            cantidad = df.iloc[i, c]
                            
                            if producto != "nan" and producto != "" and not str(cantidad).strip() in ["", "nan", "-", "0"]:
                                try:
                                    cant_val = float(cantidad)
                                    if cant_val > 0:
                                        p_raw = str(df.iloc[i, col_precio] if col_precio is not None else 0)
                                        p_val = float(re.sub(r'[^\d.]', '', p_raw.replace(',', '.')))
                                        
                                        item = {"producto": producto, "cantidad": int(cant_val), "precio_unit": p_val, "total": cant_val * p_val}
                                        resultados[rbd]["productos"].append(item)
                                        resultados[rbd]["subtotal"] += item["total"]
                                except: continue
                        break # Encontró colegio en esta columna, pasar a la siguiente columna
        
        return {k: v for k, v in resultados.items() if v["productos"]}
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        return {}