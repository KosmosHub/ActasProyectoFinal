import sqlite3
import os
from config.settings import DATABASE_PATH

def obtener_conexion():
    try:
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error BD: {e}")
        return None

def obtener_maestra_colegios():
    """Trae la lista completa de colegios con sus 3 identificadores."""
    with obtener_conexion() as conn:
        if not conn: return []
        cursor = conn.cursor()
        cursor.execute("SELECT rbd, nombre, alias FROM colegios")
        lista = [dict(row) for row in cursor.fetchall()]
        print(f"📦 Base de Datos: {len(lista)} colegios cargados.")
        return lista

def obtener_proveedores_dict():
    with obtener_conexion() as conn:
        if not conn: return {}
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT nombre, rut FROM proveedores")
            return {row['nombre']: row['rut'] for row in cursor.fetchall()}
        except: return {}

def guardar_proveedor(nombre, rut):
    with obtener_conexion() as conn:
        if not conn: return
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO proveedores (rut, nombre) VALUES (?, ?)", (rut, nombre))
        conn.commit()

def registrar_acta(d):
    with obtener_conexion() as conn:
        if not conn: return None
        cursor = conn.cursor()
        sql = """INSERT INTO actas (fecha_registro, rbd, financiamiento, orden_compra, 
                 proveedor_nombre, proveedor_rut, ruta_archivo, total) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(sql, (d['fecha_registro'], d['rbd'], d['financiamiento'], d['orden_compra'], 
                             d['proveedor_nombre'], d['proveedor_rut'], d['ruta_archivo'], d['total']))
        folio = cursor.lastrowid
        conn.commit()
        return folio

def registrar_productos(folio, lista):
    with obtener_conexion() as conn:
        if not conn: return
        cursor = conn.cursor()
        sql = "INSERT INTO productos (folio, descripcion, cantidad, precio_unit, total) VALUES (?, ?, ?, ?, ?)"
        datos = [(folio, p['producto'], p['cantidad'], p['precio_unit'], p['total']) for p in lista]
        cursor.executemany(sql, datos)
        conn.commit()