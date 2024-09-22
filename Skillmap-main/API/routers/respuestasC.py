from fastapi import APIRouter
from db.models.answersC import AnswersC
from db.schemas.answersC import answersC_schema
from db.models.questionsC import QuestionsC
from db.schemas.questionsC import questionsC_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/answersC")

def search_answers(field: str, key):
    try:
        answer = db_client.answersC.find_one({field: key})
        return AnswersC(**answersC_schema(answer))
    except:
        return False
    
def get_questions():
    try:
        question = db_client.questionsC.find_one({"_id": ObjectId("66e8e962e23a281b089a2ef8")})
        return QuestionsC(**questionsC_schema(question))
    except:
        return False

@router.post("/")
async def createDBans(answer: AnswersC):
    try:
        answer_dict = dict(answer)
        answer_dict.pop("id", None)
        answer_dict["formularioC"] = False
        
        id = db_client.answersC.insert_one(answer_dict).inserted_id
        new_answers = answersC_schema(db_client.answersC.find_one({"_id": id}))
        return {"exito": "Datos guardados"}
    except Exception as e:
        print("Error creating answers:", str(e))
        return {"error": f"Error creating answers: {str(e)}", "validation_error": answer.errors()}

@router.patch("/")
async def updateDBans(correo:str, parametro:str, valor):
    valorf = False
    print(valor)
    if valor == "true":
        valorf = True
    answer = search_answers("user_email",correo)
    answer_dict = dict(answer)
    answer_dict[parametro] = valorf
    answer_id = ObjectId(answer.id)
    try:
        db_client.answersC.update_one({"_id": answer_id}, {"$set": answer_dict})
    except Exception as e:
        return {"error": f"No se han actualizado las respuestas. Detalles del error: {str(e)}"}
    return {"exito": "Respuestas actualizadas exitosamente"}

@router.get("/")
async def answers(correo):
    answer_dict = dict(search_answers("user_email", correo))
    return answer_dict

@router.get("/preguntas")
async def questions():
    question_dict = dict(get_questions())
    return question_dict