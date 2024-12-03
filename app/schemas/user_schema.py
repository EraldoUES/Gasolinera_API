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

class User2(BaseModel):
    id_usr: int
    nombre: str
    apellido: str
    username: str
    id_rol: int
    activo: bool
    rol: Optional[str]  # El significado del id_rol

class User3(BaseModel):
    id_usr: int
    nombre: str
    apellido: str
    username: str
    id_rol: int
    activo: bool

class User4(BaseModel):
    id_usr: Optional[int]
    nombre: str
    apellido: str
    username: str
    password: str
    id_rol: int
    activo: bool

class User5(BaseModel):
    nombre: str
    apellido: str
    username: str
    password: str
    id_rol: int
    activo: bool
class LoginRequest(BaseModel):
    username: str
    password: str
