from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from db.models.user import User
from db.schemas.user import user_schema

router = APIRouter(prefix="/Skillmap")

@router.get("/")
async def read_login():
    return FileResponse("static/LOGIN/index.html")

@router.get("/Registro")
async def read_registro():
    return FileResponse("static/Registro/register.html")

@router.get("/Inicio")
async def read_inicio():
    return FileResponse("static/Inicio/index.html")

@router.get("/Dashboard")
async def read_dashboard():
    return FileResponse("static/Dashboard/dash.html")

@router.get("/RecuperarContraseña")
async def read_recuperarContraseña():
    return FileResponse("static/Contraseña/contraseña.html")

@router.get("/Contacto")
async def read_contacto():
    return FileResponse("static/Contacto/contact.html")

@router.get("/Autenticar")
async def read_autenticar():
    return FileResponse("static/Autenticacion/Auth.html")

@router.get("/AboutUs")
async def read_aboutUs():
    return FileResponse("static/AboutUs/index.html")

@router.get("/Empezar")
async def read_Empezar():
    return FileResponse("static/Empezar/index.html")

@router.get("/Empezar/Form")
async def read_Form():
    return FileResponse("static/Formulario/index.html")

@router.get("/Empezar/Activity")
async def read_Activity():
    return FileResponse("static/Actividades/index.html")