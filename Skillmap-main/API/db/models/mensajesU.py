from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class mensajesU(BaseModel):
    id: Optional[str] = None
    user_email: str
    mensaje: str
    date_time: Optional[datetime] = None