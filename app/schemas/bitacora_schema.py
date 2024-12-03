from pydantic import BaseModel
from typing import List, Optional


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
class Bitacora2(BaseModel):
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
class Bitacora3(BaseModel):
    id_bitacora: Optional[int]
    comentario: str
    km_inicial: int
    km_final: int
    num_galones: float
    costo: float
    id_tipo_combustible: int
    descripcion_tipo_combustible: str
    id_usr: int
    username: str
    id_vehiculo: int
    placa_vehiculo: str
    id_gasolinera: int
    nombre_gasolinera: str
    id_proyecto: int
    nombre_proyecto: str

class User(BaseModel):
    id_usr: int
    username: str

class Gasolinera(BaseModel):
    id_gasolinera: int
    nombre_gasolinera: str

class TipoCombustible(BaseModel):
    id_tipo_combustible: int
    descripcion_tipo_combustible: str

class Proyecto(BaseModel):
    id_proyecto: int
    nombre_proyecto: str

class Vehiculo(BaseModel):
    id_vehiculo: int
    placa_vehiculo: str

class Bitacora4(BaseModel):
    users: List[User]
    gasolineras: List[Gasolinera]
    tipos_combustible: List[TipoCombustible]
    proyectos: List[Proyecto]
    vehiculos: List[Vehiculo]
