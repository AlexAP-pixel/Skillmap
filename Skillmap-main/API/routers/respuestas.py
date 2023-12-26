from fastapi import APIRouter
from db.models.answers import Answers
from db.schemas.answers import answers_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/answers")

def search_answers(field: str, key):
    try:
        user = db_client.answers.find_one({field: key})
        return Answers(**answers_schema(user))
    except:
        return False

@router.post("/")
async def createBDans(answer: Answers):
    answer_dict = dict(answer)
    answer_dict.pop("id", None)
    id = db_client.answers.insert_one().inserted_id
    new_answers = answers_schema(db_client.answers.find_one({"_id": id}))
    return {"exito": "Datos guardados"}

@router.put("/")
async def updateDBans(answer: Answers):
    answer_dict = dict(answer)
    answer_dict.pop("id", None)
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(answer.id)}, answer_dict)
    except:
        return {"error": "No se han actualizado las respuestas"}
    return {"exito": "Respuestas guardadas"}

router.get("/")
async def answers():
    answer_dict = dict(search_answers("_id", ObjectId(id)))
    return answer_dict