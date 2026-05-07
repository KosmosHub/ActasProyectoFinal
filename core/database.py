import sqlite3
import os

DB_PATH = os.path.join("data", "BD_ActasDespacho.db")

def conectar():
    return sqlite3.connect(DB_PATH)

def guardar_proveedor(nombre, rut):
    """Inserta o actualiza un proveedor en la tabla proveedores."""
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO proveedores (rut, nombre)
            VALUES (?, ?)
            ON CONFLICT(rut) DO UPDATE SET nombre=excluded.nombre
        """, (rut, nombre))
        conn.commit()
    except Exception as e:
        print(f"❌ Error al guardar proveedor: {e}")
    finally:
        conn.close()

def obtener_proveedores_dict():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT nombre, rut FROM proveedores")
    data = {nombre: rut for nombre, rut in cur.fetchall()}
    conn.close()
    return data

def obtener_maestra_colegios():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT rbd, nombre, alias FROM colegios")
    data = [{"rbd": rbd, "nombre": nombre, "alias": alias} for rbd, nombre, alias in cur.fetchall()]
    conn.close()
    return data

def registrar_acta(datos_acta):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO actas (fecha_registro, rbd, receptor_manual, cargo_manual, financiamiento,
                           orden_compra, proveedor_nombre, proveedor_rut, ruta_archivo, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datos_acta["fecha"], datos_acta["rbd"], datos_acta.get("receptor", ""),
        datos_acta.get("cargo", ""), datos_acta["financiamiento"],
        datos_acta["orden_compra"], datos_acta["proveedor"], datos_acta["rut"],
        datos_acta["ruta_archivo"], datos_acta["total"]
    ))
    folio = cur.lastrowid
    conn.commit()
    conn.close()
    return folio

def registrar_productos(folio, productos):
    conn = conectar()
    cur = conn.cursor()
    for p in productos:
        cur.execute("""
            INSERT INTO productos (folio, descripcion, cantidad, precio_unit, total)
            VALUES (?, ?, ?, ?, ?)
        """, (
            folio, p["producto"], p.get("cantidad", 0),
            p.get("precio_unit", 0), p["total"]
        ))
    conn.commit()
    conn.close()
