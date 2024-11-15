from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.db import SessionLocal  # Importamos la sesión local
from app.models.proyecto_model import proyecto
from app.schemas.proyecto_schema import Proyecto
from typing import List

# Instancia de APIRouter
proyecto_router = APIRouter()

# Dependencia de sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los proyectos
@proyecto_router.get("/proyectos", response_model=List[Proyecto], tags=["Proyectos"])
def get_proyectos(db: Session = Depends(get_db)):
    return db.execute(proyecto.select()).fetchall()

# Obtener un proyecto por ID
@proyecto_router.get("/proyectos/{id_proyecto}", response_model=Proyecto, tags=["Proyectos"])
def get_proyecto(id_proyecto: int, db: Session = Depends(get_db)):
    proyecto_found = db.execute(proyecto.select().where(proyecto.c.id_proyecto == id_proyecto)).first()
    if not proyecto_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto not found")
    return proyecto_found

# Crear un nuevo proyecto
@proyecto_router.post("/proyectos", response_model=Proyecto, tags=["Proyectos"])
def create_proyecto(proyecto_data: Proyecto, db: Session = Depends(get_db)):
    result = db.execute(proyecto.insert().values(proyecto_data.dict()))
    db.commit()
    return db.execute(proyecto.select().where(proyecto.c.id_proyecto == result.lastrowid)).first()

# Actualizar un proyecto
@proyecto_router.put("/proyectos/{id_proyecto}", response_model=Proyecto, tags=["Proyectos"])
def update_proyecto(id_proyecto: int, proyecto_data: Proyecto, db: Session = Depends(get_db)):
    db.execute(proyecto.update().where(proyecto.c.id_proyecto == id_proyecto).values(proyecto_data.dict()))
    db.commit()
    return db.execute(proyecto.select().where(proyecto.c.id_proyecto == id_proyecto)).first()

# Eliminar un proyecto por ID
@proyecto_router.delete("/proyectos/{id_proyecto}", status_code=status.HTTP_204_NO_CONTENT, tags=["Proyectos"])
def delete_proyecto(id_proyecto: int, db: Session = Depends(get_db)):
    db.execute(proyecto.delete().where(proyecto.c.id_proyecto == id_proyecto))
    db.commit()
    return {"message": "Proyecto deleted"}

