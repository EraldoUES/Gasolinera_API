from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id_usr: Optional[int]
    nombre: str
    apellido: str
    username: str
    password: str
    id_rol: int
    activo: Optional[bool] = True
