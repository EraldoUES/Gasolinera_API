from pydantic import BaseModel
from typing import Optional

class Proyecto(BaseModel):
    id_proyecto: Optional[int]
    nombre: str
    direccion: str
    activo: Optional[bool] = True