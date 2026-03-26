import sqlite3
import os

# 👉 Ruta absoluta de la base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "travel_ai.db")


def crear_base_datos():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    # 👉 Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        plan TEXT DEFAULT 'free'
    )
    """)

    # 👉 Tabla de uso (para limitar consultas)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        consultas INTEGER DEFAULT 0
    )
    """)

    conexion.commit()
    conexion.close()