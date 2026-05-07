import pandas as pd
import re
import difflib

def cargar_excel(ruta_excel):
    """Carga todas las hojas de un archivo Excel en un diccionario."""
    try:
        xls = pd.ExcelFile(ruta_excel)
        hojas = {nombre: xls.parse(nombre) for nombre in xls.sheet_names}
        return hojas
    except Exception as e:
        print(f"❌ Error al cargar el Excel: {e}")
        return None

def detectar_hoja_valida(hojas):
    """Detecta la hoja con más datos (filas x columnas)."""
    if not hojas:
        return None
    hoja_valida = None
    max_celdas = 0
    for nombre, df in hojas.items():
        celdas = df.shape[0] * df.shape[1]
        if celdas > max_celdas:
            max_celdas = celdas
            hoja_valida = df
    return hoja_valida

def normalizar(texto):
    if not texto or pd.isna(texto): 
        return ""
    t = str(texto).upper()
    t = re.sub(r'[.\-,\(\)°#]', ' ', t)
    return " ".join(t.split())

def mejor_match(nombre_col, maestra_prep):
    """
    Busca coincidencia difusa palabra por palabra entre nombre de columna y colegios de la BD.
    """
    mejor_rbd = None
    mejor_nombre = nombre_col
    mejor_score = 0.0

    palabras_col = nombre_col.split()

    for c in maestra_prep:
        for candidato in [c["nombre"], c["alias"], c["rbd"]]:
            if not candidato:
                continue
            for palabra in palabras_col:
                score = difflib.SequenceMatcher(None, palabra, candidato).ratio()
                if score > mejor_score:
                    mejor_score = score
                    mejor_rbd = c["rbd"]
                    mejor_nombre = c["original"]

    # 🔹 Umbral bajo (0.4 = 40%)
    if mejor_score >= 0.4:
        return mejor_rbd, mejor_nombre
    else:
        return None, nombre_col

def agrupar_por_columnas(df, maestra_colegios):
    """
    Recorre columnas de distribución (ej: POLITECNICO, ESTELA AVILA, ARTURO ALESSANDRI)
    y genera un acta por cada colegio con sus productos.
    """
    grupos = {}

    # Preparamos lista de nombres y alias normalizados
    maestra_prep = []
    for c in maestra_colegios:
        maestra_prep.append({
            "rbd": c.get('rbd', ''),
            "nombre": normalizar(c.get('nombre', '')),
            "alias": normalizar(c.get('alias', '')),
            "original": c.get('nombre', '')
        })

    columnas_fijas = ["ITEM N°", "Productos solicitados", "UNIDAD MET.", "CANTIDADES", "PRECIO", "IMAGEN REFERENCIAL", "TOTAL"]
    columnas_colegios = [col for col in df.columns if col not in columnas_fijas]

    for col in columnas_colegios:
        nombre_col = normalizar(col)
        colegio_rbd, colegio_nombre = mejor_match(nombre_col, maestra_prep)

        if not colegio_rbd:
            colegio_rbd = nombre_col
            colegio_nombre = col

        productos_colegio = []

        # Recorremos filas y tomamos productos
        for _, fila in df.iterrows():
            producto = str(fila.get("Productos solicitados", "")).strip()
            cantidad = fila.get(col, None)
            precio_unit = fila.get("PRECIO", None)

            if not producto or pd.isna(cantidad) or cantidad == "-" or cantidad == 0:
                continue

            try:
                cantidad_val = int(cantidad)
                precio_val = float(str(precio_unit).replace('$', '').replace('.', '').replace(',', ''))
                total_val = cantidad_val * precio_val

                productos_colegio.append({
                    "producto": producto,
                    "cantidad": cantidad_val,
                    "total": total_val
                })
            except:
                continue

        # 🔹 Solo agregamos el colegio si tiene productos
        if productos_colegio:
            subtotal = sum(p["total"] for p in productos_colegio)
            iva = subtotal * 0.19
            total_con_iva = subtotal + iva

            grupos[colegio_rbd] = {
                "nombre": colegio_nombre,
                "productos": productos_colegio,
                "subtotal": subtotal,
                "iva": iva,
                "total_con_iva": total_con_iva
            }

    # 🔹 Si no se detectó nada, devolvemos vacío pero con aviso
    return grupos
