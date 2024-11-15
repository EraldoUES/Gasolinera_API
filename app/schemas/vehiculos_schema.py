from pydantic import BaseModel
from typing import Optional

class Vehiculo(BaseModel):
    id_vehiculo: Optional[int]
    modelo: str
    marca: str
    placa: str
    rendimiento: float
    galonaje: float
    id_tipo_combustible: int
