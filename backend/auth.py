import sqlite3
import os
from fastapi import APIRouter, HTTPException

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "travel_ai.db")


# 🔐 REGISTRO
@router.post("/registro")
def registro(email: str, password: str):

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email y contraseña obligatorios")

    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO usuarios (email, password) VALUES (?, ?)",
            (email, password)
        )

        conexion.commit()
        conexion.close()

        return {"mensaje": "Usuario creado correctamente"}

    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🔐 LOGIN
@router.post("/login")
def login(email: str, password: str):

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email y contraseña obligatorios")

    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email=? AND password=?",
            (email, password)
        )

        usuario = cursor.fetchone()
        conexion.close()

        if not usuario:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")

        return {
            "mensaje": "Login correcto",
            "usuario": {
                "id": usuario[0],
                "email": usuario[1],
                "plan": usuario[3]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🚀 UPGRADE A PRO
@router.post("/upgrade")
def upgrade(email: str):

    if not email:
        raise HTTPException(status_code=400, detail="Email requerido")

    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute(
            "UPDATE usuarios SET plan='pro' WHERE email=?",
            (email,)
        )

        conexion.commit()
        conexion.close()

        return {"mensaje": "Usuario actualizado a PRO"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 👤 PERFIL USUARIO
@router.get("/perfil")
def perfil(email: str):

    if not email:
        raise HTTPException(status_code=400, detail="Email requerido")

    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        # 👉 Obtener plan
        cursor.execute(
            "SELECT plan FROM usuarios WHERE email=?",
            (email,)
        )
        usuario = cursor.fetchone()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # 👉 Obtener uso
        cursor.execute(
            "SELECT consultas FROM uso WHERE email=?",
            (email,)
        )
        uso = cursor.fetchone()

        conexion.close()

        consultas = uso[0] if uso else 0

        return {
            "email": email,
            "plan": usuario[0],
            "consultas": consultas
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))