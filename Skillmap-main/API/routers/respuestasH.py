from fastapi import APIRouter
from db.models.answersH import AnswersH
from db.schemas.answersH import answersH_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/answersH")

def search_answers(field: str, key):
    try:
        answer = db_client.answersH.find_one({field: key})
        return AnswersH(**answersH_schema(answer))
    except:
        return False

@router.post("/")
async def createDBans(answer: AnswersH):
    try:
        answer_dict = dict(answer)
        answer_dict.pop("id", None)
        answer_dict["formularioH"] = False
        
        id = db_client.answersH.insert_one(answer_dict).inserted_id
        new_answers = answersH_schema(db_client.answersH.find_one({"_id": id}))
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
        db_client.answersH.update_one({"_id": answer_id}, {"$set": answer_dict})
    except Exception as e:
        return {"error": f"No se han actualizado las respuestas. Detalles del error: {str(e)}"}
    return {"exito": "Respuestas actualizadas exitosamente"}

@router.get("/")
async def answers(correo):
    answer_dict = dict(search_answers("user_email", correo))
    return answer_dict