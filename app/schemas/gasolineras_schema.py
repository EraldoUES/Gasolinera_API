from pydantic import BaseModel
from typing import Optional

class Gasolinera(BaseModel):
    id_gasolinera: Optional[int]
    nombre: str
    direccion: str
class Gasolinera2(BaseModel):
    nombre: str
    direccion: str
