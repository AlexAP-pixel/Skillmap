def answers_schema(answers) -> dict:
    return{"id": str(answers["_id"]),
           "user_email": answers["user_email"],
           "res1": answers["res1"],
           "res2": answers["res2"],
           "res3": answers["res3"],
           "res4": answers["res4"],
           "res5": answers["res5"],
           "res6": answers["res6"],
           "res7": answers["res7"],
           "res8": answers["res8"],
           "res9": answers["res9"],
           "res10": answers["res10"],
           "res11": answers["res11"],
           "res12": answers["res12"],
           "res13": answers["res13"],
           "act1": answers["act1"],
           "act2": answers["act2"],
           "act3": answers["act3"],
           "act4": answers["act4"],
           "formulario": answers["formulario"],
           "actividades": answers["actividades"]}