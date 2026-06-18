import sqlite3
import os

DB_FILE = "base_datos.db"

def inicializar_db():
    """Crea el archivo .db y las tablas relacionales si no existen"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Tabla de Pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY,
            cliente TEXT NOT NULL,
            direccion TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    ''')
    
    # Tabla de Repartidores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS repartidores (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            disponible INTEGER DEFAULT 1
        )
    ''')
    
    # Tabla de Incidencias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            gravedad TEXT NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def obtener_conexion():
    inicializar_db()
    return sqlite3.connect(DB_FILE)