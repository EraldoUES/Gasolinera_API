from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.db import SessionLocal  # Importamos la sesión local
from app.models.tipo_combustible_model import tipo_combustible
from app.schemas.tipo_combustible_schema import TipoCombustible
from typing import List

# Instancia APIRouter
tipo_combustible_router = APIRouter()

# Dependencia de sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los tipos de combustible
@tipo_combustible_router.get("/tipos_combustible", response_model=List[TipoCombustible], tags=["Tipos Combustible"])
def get_tipos_combustible(db: Session = Depends(get_db)):
    return db.execute(tipo_combustible.select()).fetchall()

# Obtener tipo de combustible por ID
@tipo_combustible_router.get("/tipos_combustible/{id_tipo_combustible}", response_model=TipoCombustible, tags=["Tipos Combustible"])
def get_tipo_combustible(id_tipo_combustible: int, db: Session = Depends(get_db)):
    tipo_found = db.execute(tipo_combustible.select().where(tipo_combustible.c.id_tipo_combustible == id_tipo_combustible)).first()
    if not tipo_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TipoCombustible not found")
    return tipo_found

# Crear tipo de combustible
@tipo_combustible_router.post("/tipos_combustible", response_model=TipoCombustible, tags=["Tipos Combustible"])
def create_tipo_combustible(tipo_data: TipoCombustible, db: Session = Depends(get_db)):
    result = db.execute(tipo_combustible.insert().values(tipo_data.dict()))
    db.commit()
    return db.execute(tipo_combustible.select().where(tipo_combustible.c.id_tipo_combustible == result.lastrowid)).first()

# Actualizar tipo de combustible
@tipo_combustible_router.put("/tipos_combustible/{id_tipo_combustible}", response_model=TipoCombustible, tags=["Tipos Combustible"])
def update_tipo_combustible(id_tipo_combustible: int, tipo_data: TipoCombustible, db: Session = Depends(get_db)):
    db.execute(tipo_combustible.update().where(tipo_combustible.c.id_tipo_combustible == id_tipo_combustible).values(tipo_data.dict()))
    db.commit()
    return db.execute(tipo_combustible.select().where(tipo_combustible.c.id_tipo_combustible == id_tipo_combustible)).first()

# Eliminar tipo de combustible
@tipo_combustible_router.delete("/tipos_combustible/{id_tipo_combustible}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tipos Combustible"])
def delete_tipo_combustible(id_tipo_combustible: int, db: Session = Depends(get_db)):
    db.execute(tipo_combustible.delete().where(tipo_combustible.c.id_tipo_combustible == id_tipo_combustible))
    db.commit()
    return {"message": "TipoCombustible deleted"}
