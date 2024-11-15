from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.db import SessionLocal  # Importamos la sesión local
from app.models.rol_model import rol
from app.schemas.rol_schema import Rol
from typing import List

# Instancia de APIRouter
rol_router = APIRouter()

# Dependencia de sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los roles
@rol_router.get("/roles", response_model=List[Rol], tags=["Roles"])
def get_roles(db: Session = Depends(get_db)):
    return db.execute(rol.select()).fetchall()

# Obtener rol por ID
@rol_router.get("/roles/{id_rol}", response_model=Rol, tags=["Roles"])
def get_rol(id_rol: int, db: Session = Depends(get_db)):
    rol_found = db.execute(rol.select().where(rol.c.id_rol == id_rol)).first()
    if not rol_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol not found")
    return rol_found

# Crear nuevo rol
@rol_router.post("/roles", response_model=Rol, tags=["Roles"])
def create_rol(rol_data: Rol, db: Session = Depends(get_db)):
    result = db.execute(rol.insert().values(rol_data.dict()))
    db.commit()
    return db.execute(rol.select().where(rol.c.id_rol == result.lastrowid)).first()

# Actualizar rol
@rol_router.put("/roles/{id_rol}", response_model=Rol, tags=["Roles"])
def update_rol(id_rol: int, rol_data: Rol, db: Session = Depends(get_db)):
    db.execute(rol.update().where(rol.c.id_rol == id_rol).values(rol_data.dict()))
    db.commit()
    return db.execute(rol.select().where(rol.c.id_rol == id_rol)).first()

# Eliminar un rol
@rol_router.delete("/roles/{id_rol}", status_code=status.HTTP_204_NO_CONTENT, tags=["Roles"])
def delete_rol(id_rol: int, db: Session = Depends(get_db)):
    db.execute(rol.delete().where(rol.c.id_rol == id_rol))
    db.commit()
    return {"message": "Rol deleted"}

