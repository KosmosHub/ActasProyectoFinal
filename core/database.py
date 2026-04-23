import sqlite3

DATABASE_PATH = "data/actas.db"

def conectar():
    return sqlite3.connect(DATABASE_PATH)

def registrar_acta(datos, ruta_pdf):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO actas (fecha, nrc, receptor, cargo, financiamiento,
                           orden_compra, factura, guia, proveedor, rut, archivo, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datos["fecha"], datos["nrc"], datos["receptor"], datos["cargo"],
        datos["financiamiento"], datos["orden_compra"], datos["factura"],
        datos["guia"], datos["proveedor"], datos["rut"], ruta_pdf, datos["total"]
    ))

    folio = cursor.lastrowid
    conn.commit()
    conn.close()
    return folio

def registrar_productos(folio, productos):
    conn = conectar()
    cursor = conn.cursor()
    for p in productos:
        cursor.execute("""
            INSERT INTO productos (folio, producto, cantidad, precio_unit, total)
            VALUES (?, ?, ?, ?, ?)
        """, (folio, p["producto"], p["cantidad"], p["precio_unit"], p["total"]))
    conn.commit()
    conn.close()
