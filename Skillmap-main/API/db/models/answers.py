from pydantic import BaseModel
from typing import Optional

class Answers(BaseModel):
    id: Optional[str] = None
    user_id: str
    res1: str
    res2: str
    res3: str
    res4: str
    res5: int
    res6: int
    res7: str
    res8: str
    res9: int