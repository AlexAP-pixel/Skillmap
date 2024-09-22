from fastapi import APIRouter
from db.models.answersK import AnswersK
from db.schemas.answersK import answersK_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/answersK")

def search_answers(field: str, key):
    try:
        answer = db_client.answersK.find_one({field: key})
        return AnswersK(**answersK_schema(answer))
    except:
        return False

@router.post("/")
async def createDBans(answer: AnswersK):
    try:
        answer_dict = dict(answer)
        answer_dict.pop("id", None)
        answer_dict["formularioK"] = False
        
        id = db_client.answersK.insert_one(answer_dict).inserted_id
        new_answers = answersK_schema(db_client.answersK.find_one({"_id": id}))
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
        db_client.answersK.update_one({"_id": answer_id}, {"$set": answer_dict})
    except Exception as e:
        return {"error": f"No se han actualizado las respuestas. Detalles del error: {str(e)}"}
    return {"exito": "Respuestas actualizadas exitosamente"}

@router.get("/")
async def answers(correo):
    answer_dict = dict(search_answers("user_email", correo))
    return answer_dict