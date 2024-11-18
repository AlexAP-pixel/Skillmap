import os
from fastapi import APIRouter
from fastapi import Request
from db.models.results import Result
from db.schemas.results import result_schema
from db.models.user import User
from db.schemas.user import user_schema
from db.models.carreras import Carrera
from db.schemas.carreras import carrera_schema
from db.models.escuelas import Escuela
from db.schemas.escuelas import escuela_schema
from db.client import db_client
from bson import ObjectId
from moviepy.editor import VideoFileClip, concatenate_videoclips

router = APIRouter(prefix="/resultados")

def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return False
    
def search_result(field: str, key):
    try:
        result = db_client.results.find_one({field: key})
        if(result == None):
            return False
        return True
    except:
        return False
    
def calculated_result(field: str, key):
    try:
        result = db_client.results.find_one({field: key})
        return Result(**result_schema(result))
    except:
        return False

@router.get("/calculos")
async def validate_results(correo: str):
    user = search_user("correo", correo)
    idUsuario = user.id
    consultaResult = search_result("id_usuario", idUsuario)
    if consultaResult:
        return {"exito": "El usuario ya tiene base de resultados"}
    return {"error": "El usuario aun no cuenta con resultados"}

@router.get("/")
async def get_results(correo: str):
    user = search_user("correo", correo)
    idUsuario = user.id
    result = calculated_result("id_usuario", idUsuario)
    if not result:
        return {"error": "No se encontro el usuario"}
    return {"exito": result}
    
    
@router.put("/video")
async def set_video(correo: str):
    try:
        directorio = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'Videos')
        directorio = os.path.normpath(directorio)
        
        user = search_user("correo", correo)
        idUsuario = user.id
        resultados = calculated_result("id_usuario", idUsuario)
        
        if not resultados:
            print("No se encontraron resultados")
            return {"error": "No se encontraron resultados para este usuario"}
        
        video_path = os.path.join(directorio, f"{idUsuario}.mp4")
        if os.path.exists(video_path):
            return {"exito": f"{idUsuario}.mp4"}
        
        videos = []
        for i in range(1, 6):
            id_key = f"id_carrera{i}"
            carrera_id = getattr(resultados, id_key, None)
            if carrera_id:
                carrera = db_client.carreras.find_one({"_id": ObjectId(carrera_id)})
                video = carrera.get("video", " ")
                video += '.mp4'
                num = str(i) + ".mp4"
                videos.append(num)
                videos.append(video)
        
        clips = []
        for video in videos:
            video_path = os.path.join(directorio, video)
            if not os.path.exists(video_path):
                print(f"Error: El archivo {video} no existe en la ruta {video_path}")
                return {"error": f"El archivo de video {video} no se encuentra."}
            clip = VideoFileClip(video_path)
            clips.append(clip)
        
        final_video = concatenate_videoclips(clips)
        output_path = os.path.join(directorio, f"{idUsuario}.mp4")
        final_video.write_videofile(output_path, codec="libx264", threads=4, preset='ultrafast')
        
        return {"exito": f"{idUsuario}.mp4"}
    
    except Exception as e:
        print(f"Error al procesar los videos: {str(e)}")
        return {"error": f"Ocurrió un error: {str(e)}"}
    
    
@router.post("/")
async def create_results(result: Result):
    user = search_user("correo", result.id_usuario)
    idUsuario = user.id
    consultaResult = search_result("id_usuario", idUsuario)
    if consultaResult:
        return {"error": "El usuario ya tiene base de resultados"}
    
    carreras = list(db_client.carreras.find())
    IA = [(i / 28) * 10 for i in range(7, 0, -1)]
    D = [(i / 21) * 10 for i in range(6, 0, -1)]
    EI = [(i / 55) * 10 for i in range(10, 0, -1)]
    I1, I2, I3, I4, I5, I6, I7 = IA
    A1, A2, A3, A4, A5, A6, A7 = IA
    D1, D2, D3, D4, D5, D6 = D
    EI1, EI2, EI3, EI4, EI5, EI6, EI7, EI8, EI9, EI10 = EI
    valores =[
        (result.In1, I1),
        (result.In2, I2),
        (result.In3, I3),
        (result.In4, I4),
        (result.In5, I5),
        (result.In6, I6),
        (result.In7, I7),
        (result.Ha1, A1),
        (result.Ha2, A2),
        (result.Ha3, A3),
        (result.Ha4, A4),
        (result.Ha5, A5),
        (result.Ha6, A6),
        (result.Ha7, A7),
        (result.D1, D1),
        (result.D2, D2),
        (result.D3, D3),
        (result.D4, D4),
        (result.D5, D5),
        (result.D6, D6),
        (result.EI1, EI1),
        (result.EI2, EI2),
        (result.EI3, EI3),
        (result.EI4, EI4),
        (result.EI5, EI5),
        (result.EI6, EI6),
        (result.EI7, EI7),
        (result.EI8, EI8),
        (result.EI9, EI9),
        (result.EI10, EI10)
    ]
    listCarreras = []
    
    for carrera in carreras:
        puntaje = 0
        id = str(carrera.get("_id", "Campo no encontrado"))
        val_C = carrera.get("C", [])
        cant_C = len(val_C)
        for elemC in val_C:
            for val in valores:
                primer = val[0]
                if primer[0] in elemC:
                    puntaje += (val[1] / cant_C)
        val_K = carrera.get("K", [])
        cant_K = len(val_K)
        for elemK in val_K:
            for val in valores:
                primer = val[0]
                if primer in elemK:
                    puntaje += (val[1] / cant_K)
        val_H = carrera.get("H", [])
        cant_H = len(val_H)
        for elemH in val_H:
            for val in valores:
                primer = val[0]
                if primer in elemH:
                    puntaje += (val[1] / cant_H)
        listCarreras.append((id, puntaje))
    
    listCarreras.sort(key=lambda x: x[1], reverse=True)
    
    result_dict = dict(result)
    
    for i in range(8):
        result_dict[f"id_carrera{i+1}"] = listCarreras[i][0]
        result_dict[f"val_carrera{i+1}"] = listCarreras[i][1]
        
    result_dict["id_usuario"] = idUsuario
    result_dict.pop("id", None)
    
    db_client.results.insert_one(result_dict)
    return {"exito": "Resultados guardados"}

@router.put("/")
async def update_resultados(correo: str):
    user = search_user("correo", correo)
    idUsuario = user.id
    resultados = calculated_result("id_usuario", idUsuario)
    if not resultados:
        print("No se encontraron resultados")
        return {"error": "No se encontraron resultados para este usuario"}

    try:
        db_client.results.update_one({"_id": ObjectId(resultados.id)},{"$set": {"Actividad": True}})
    except:
        return {"error": "No se actualizo el estatus de actividad"}
    
    return {"exito": "Se registro la actividad"}