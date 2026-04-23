import pandas as pd

def cargar_excel(ruta_archivo):
    try:
        hojas = pd.read_excel(ruta_archivo, sheet_name=None, header=None)  # sin encabezados
        return hojas
    except Exception as e:
        print(f"Error al cargar el Excel: {e}")
        return None

def detectar_hoja_valida(hojas):
    for nombre, df in hojas.items():
        if df.shape[0] > 5 and df.shape[1] > 2:
            print(f"Hoja detectada: {nombre}")
            return df
    return None

def agrupar_por_filas(df):
    """
    Detecta colegios en filas y agrupa productos asociados.
    Supone que:
    - Una fila con un solo valor de texto = nombre del colegio.
    - Las filas siguientes contienen productos, cantidades y precios.
    """
    grupos = {}
    colegio_actual = None

    for _, fila in df.iterrows():
        valores = [str(v).strip() for v in fila if pd.notna(v)]
        if len(valores) == 1 and not valores[0].isdigit():
            # Detectamos un nombre de colegio
            colegio_actual = valores[0]
            grupos[colegio_actual] = []
        elif colegio_actual and len(valores) >= 3:
            try:
                producto = valores[0]
                cantidad = int(valores[1])
                precio = float(valores[2])
                grupos[colegio_actual].append({
                    "producto": producto,
                    "cantidad": cantidad,
                    "precio_unit": precio,
                    "total": cantidad * precio
                })
            except Exception:
                continue

    return grupos
