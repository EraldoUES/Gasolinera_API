from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Log(BaseModel):
    id_log: Optional[int]
    descripcion: str
    id_usr: int
    fecha: Optional[datetime] = None
class Log2(BaseModel):
    id_log: Optional[int]
    descripcion: str
    id_usr: int
    username: str
    fecha: Optional[datetime] = None