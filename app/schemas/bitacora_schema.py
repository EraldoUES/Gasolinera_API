from pydantic import BaseModel
from typing import Optional

class Bitacora(BaseModel):
    id_bitacora: Optional[int]
    comentario: str
    km_inicial: int
    km_final: int
    num_galones: float
    costo: float
    id_tipo_combustible: int
    id_usr: int
    id_vehiculo: int
    id_gasolinera: int
    id_proyecto: int
