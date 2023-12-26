def answers_schema(answers) -> dict:
    return{"id": str(answers["_id"]),
           "user_id": answers["user_id"],
           "res1": answers["res1"],
           "res2": answers["res2"],
           "res3": answers["res3"],
           "res4": answers["res4"],
           "res5": answers["res5"],
           "res6": answers["res6"],
           "res7": answers["res7"],
           "res8": answers["res8"],
           "res9": answers["res9"]}