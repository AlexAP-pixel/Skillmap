from pydantic import BaseModel
from typing import Optional

class Answers(BaseModel):
    id: Optional[str] = None
    user_email: str
    res1: str
    res2: str
    res3: str
    res4: str
    res5: str
    res6: str
    res7: str
    res8: str
    res9: str
    res10: str
    res11: str
    res12: str
    res13: str
    act1: int
    act2: int
    act3: int
    act4: int
    formulario: Optional[bool] = None
    actividades: Optional[bool] = None
    