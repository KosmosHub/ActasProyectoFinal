import pandas as pd
import re
from core.database import obtener_maestra_colegios

def limpiar_texto(t):
    """Normaliza el texto para comparaciones seguras."""
    return re.sub(r'[^A-Z0-9]', '', str(t).upper()) if t else ""

def agrupar_por_columnas(ruta_excel):
    """
    Escaneo por coordenadas con validación de integridad para evitar colegios fantasma.
    """
    maestra = obtener_maestra_colegios()
    if not maestra: return {}

    try:
        # Cargamos el Excel sin encabezados para mapear la matriz real
        df = pd.read_excel(ruta_excel, header=None)
        resultados = {}

        # 1. Localizar el "Ancla" de la tabla (Productos y Precios)
        fila_encabezados = 0
        col_prod, col_precio = None, None

        for r in range(min(20, len(df))):
            fila_str = df.iloc[r].astype(str).str.upper()
            if fila_str.str.contains("PRODUCTOS SOLICITADOS").any():
                fila_encabezados = r
                col_prod = fila_str.str.contains("PRODUCTOS SOLICITADOS").idxmax()
                break
        
        if col_prod is None: return {}

        # Localizar columna de precio unitario en la misma fila
        fila_headers = df.iloc[fila_encabezados].astype(str).str.upper()
        if fila_headers.str.contains("PRECIO").any():
            col_precio = fila_headers.str.contains("PRECIO").idxmax()

        # 2. Identificar columnas de Colegios
        for c in range(len(df.columns)):
            val_celda = str(df.iloc[fila_encabezados, c]).upper()
            
            # Saltamos columnas que sabemos que no son colegios
            if any(x in val_celda for x in ["ITEM", "PRODUCTO", "UNIDAD", "CANTIDAD", "PRECIO", "TOTAL", "IMAGEN", "NAN"]):
                continue

            for m in maestra:
                nom_db = limpiar_texto(m['nombre'])
                alias_db = limpiar_texto(m.get('alias', ''))
                val_excel = limpiar_texto(val_celda)

                # Validación de coincidencia (Intuición)
                if val_excel and (val_excel in nom_db or (alias_db and alias_db in val_excel)):
                    rbd = m['rbd']
                    productos_colegio = []
                    subtotal_acumulado = 0

                    # 3. Extraer productos para este colegio específico
                    for r in range(fila_encabezados + 1, len(df)):
                        desc_prod = str(df.iloc[r, col_prod]).strip()
                        cantidad = df.iloc[r, c]
                        
                        # Validamos que haya una descripción y una cantidad numérica real
                        if desc_prod and desc_prod != "nan":
                            try:
                                cant_val = float(cantidad)
                                if cant_val > 0:
                                    p_raw = str(df.iloc[r, col_precio] if col_precio is not None else 0)
                                    p_val = float(re.sub(r'[^\d.]', '', p_raw.replace(',', '.')))
                                    
                                    productos_colegio.append({
                                        "producto": desc_prod,
                                        "cantidad": int(cant_val),
                                        "precio_unit": p_val,
                                        "total": cant_val * p_val
                                    })
                                    subtotal_acumulado += (cant_val * p_val)
                            except: continue

                    # CRÍTICO: Solo agregar el colegio si realmente tiene productos detectados
                    if productos_colegio:
                        resultados[rbd] = {
                            "nombre": m['nombre'],
                            "productos": productos_colegio,
                            "subtotal": subtotal_acumulado
                        }
                    break # Salir del bucle de maestra para esta columna

        return resultados
    except Exception as e:
        print(f"❌ Error en la extracción: {e}")
        return {}