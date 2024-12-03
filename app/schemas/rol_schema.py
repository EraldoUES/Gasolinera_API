from pydantic import BaseModel
from typing import Optional

class Rol(BaseModel):
    id_rol: Optional[int]
    descripcion: str
class Rol2(BaseModel):
    descripcion: str
