from fastapi import APIRouter
from db.models.answers import Answers
from db.schemas.answers import answers_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/answers")

def search_answers(field: str, key):
    try:
        answer = db_client.answers.find_one({field: key})
        return Answers(**answers_schema(answer))
    except:
        return False

@router.post("/")
async def createDBans(answer: Answers):
    try:
        answer_dict = dict(answer)
        answer_dict.pop("id", None)
        answer_dict["formulario"] = False
        answer_dict["actividades"] = False
        
        id = db_client.answers.insert_one(answer_dict).inserted_id
        new_answers = answers_schema(db_client.answers.find_one({"_id": id}))
        print("Formato de respuestas creado")
        return {"exito": "Datos guardados"}
    except Exception as e:
        print("Error creating answers:", str(e))
        return {"error": f"Error creating answers: {str(e)}", "validation_error": answer.errors()}

@router.patch("/")
async def updateDBans(correo:str, parametro:str, valor):
    if valor == "true":
        valor = True
    elif valor == "false":
        valor = False
    answer = search_answers("user_email",correo)
    answer_dict = dict(answer)
    answer_dict[parametro] = valor
    answer_id = ObjectId(answer.id)
    try:
        db_client.answers.update_one({"_id": answer_id}, {"$set": answer_dict})
    except Exception as e:
        return {"error": f"No se han actualizado las respuestas. Detalles del error: {str(e)}"}
    return {"exito": "Respuestas actualizadas exitosamente"}

@router.get("/")
async def answers(correo):
    answer_dict = dict(search_answers("user_email", correo))
    return answer_dict