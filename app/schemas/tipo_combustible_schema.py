from pydantic import BaseModel
from typing import Optional

class TipoCombustible(BaseModel):
    id_tipo_combustible: Optional[int]
    descripcion: str