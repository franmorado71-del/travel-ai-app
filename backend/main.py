from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.recomendador import recomendar_destinos
from backend.auth import router as auth_router
from backend.database import crear_base_datos
from backend.uso import obtener_uso, incrementar_uso

import sqlite3
import os

app = FastAPI(title="Travel AI API")

# 👉 Crear base de datos
crear_base_datos()

# 👉 Rutas auth
app.include_router(auth_router)

# 👉 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 👉 SERVIR FRONTEND (ESTE ES EL QUE FUNCIONA SIEMPRE)
@app.get("/")
def home():
    return FileResponse("frontend/index.html")


# 👉 DB path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "travel_ai.db")


def obtener_plan(email):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute("SELECT plan FROM usuarios WHERE email=?", (email,))
    resultado = cursor.fetchone()

    conexion.close()

    return resultado[0] if resultado else "free"


@app.get("/recomendar")
def recomendar(presupuesto: int, tipo: str, email: str):

    plan = obtener_plan(email)

    if plan == "free":
        uso_actual = obtener_uso(email)

        if uso_actual >= 3:
            return {"error": "Límite FREE alcanzado"}

        incrementar_uso(email)

        return {
            "plan": "free",
            "consultas_usadas": uso_actual + 1,
            "recomendaciones": recomendar_destinos(presupuesto, tipo)
        }

    return {
        "plan": "pro",
        "recomendaciones": recomendar_destinos(presupuesto, tipo)
    }


import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=10000)