def mensajesU_schema(mensajesU) -> dict:
    return{"id": str(mensajesU["_id"]),
           "user_email": mensajesU["user_email"],
           "mensaje": mensajesU["mensaje"],
           "date_time": mensajesU["date_time"]}