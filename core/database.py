import sqlite3
import os
from config.settings import DATABASE_PATH

def conectar():
    return sqlite3.connect(DATABASE_PATH)

def obtener_maestra_colegios():
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute("SELECT rbd, nombre, alias FROM colegios")
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()

def obtener_proveedores_dict():
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("SELECT nombre, rut FROM proveedores")
        return {nombre: rut for nombre, rut in cur.fetchall()}
    finally:
        conn.close()

def guardar_proveedor(nombre, rut):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO proveedores (rut, nombre) VALUES (?, ?) ON CONFLICT(rut) DO UPDATE SET nombre=excluded.nombre", (rut, nombre))
        conn.commit()
    finally:
        conn.close()

def registrar_acta(d):
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO actas (fecha_registro, rbd, receptor_manual, cargo_manual, financiamiento, 
                               orden_compra, proveedor_nombre, proveedor_rut, ruta_archivo, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (d["fecha"], d["rbd"], d.get("receptor", ""), d.get("cargo", ""), d["financiamiento"],
              d["orden_compra"], d["proveedor"], d["rut"], d["ruta_archivo"], d["total"]))
        folio = cur.lastrowid
        conn.commit()
        return folio
    finally:
        conn.close()

def registrar_productos(folio, lista):
    conn = conectar()
    cur = conn.cursor()
    try:
        for p in lista:
            cur.execute("INSERT INTO productos (folio, descripcion, cantidad, precio_unit, total) VALUES (?, ?, ?, ?, ?)",
                        (folio, p["producto"], p["cantidad"], p["precio_unit"], p["total"]))
        conn.commit()
    finally:
        conn.close()