import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "travel_ai.db")

LIMITE_FREE = 3


def obtener_uso(email):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("SELECT consultas FROM uso WHERE email=?", (email,))
    resultado = cursor.fetchone()

    conexion.close()

    if resultado:
        return resultado[0]
    else:
        return 0


def incrementar_uso(email):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("SELECT consultas FROM uso WHERE email=?", (email,))
    resultado = cursor.fetchone()

    if resultado:
        cursor.execute(
            "UPDATE uso SET consultas = consultas + 1 WHERE email=?",
            (email,)
        )
    else:
        cursor.execute(
            "INSERT INTO uso (email, consultas) VALUES (?, 1)",
            (email,)
        )

    conexion.commit()
    conexion.close()