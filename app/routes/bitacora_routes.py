from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.db import SessionLocal  # Importamos la sesión local
from app.models.bitacora_model import bitacora
from app.schemas.bitacora_schema import Bitacora
from typing import List

# Instancia de APIRouter
bitacora_router = APIRouter()

# Dependencia de sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todas las entradas de bitacora
@bitacora_router.get("/bitacora", response_model=List[Bitacora], tags=["Bitacora"])
def get_bitacora_entries(db: Session = Depends(get_db)):
    return db.execute(bitacora.select()).fetchall()

# Obtener una entrada específica de bitacora por ID
@bitacora_router.get("/bitacora/{id_bitacora}", response_model=Bitacora, tags=["Bitacora"])
def get_bitacora_entry(id_bitacora: int, db: Session = Depends(get_db)):
    bitacora_entry = db.execute(bitacora.select().where(bitacora.c.id_bitacora == id_bitacora)).first()
    if not bitacora_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bitacora entry not found")
    return bitacora_entry

# Crear una nueva entrada en bitacora
@bitacora_router.post("/bitacora", response_model=Bitacora, tags=["Bitacora"])
def create_bitacora_entry(entry: Bitacora, db: Session = Depends(get_db)):
    result = db.execute(bitacora.insert().values(entry.dict()))
    db.commit()
    return db.execute(bitacora.select().where(bitacora.c.id_bitacora == result.lastrowid)).first()

# Actualizar una entrada de la bitacora
@bitacora_router.put("/bitacora/{id_bitacora}", response_model=Bitacora, tags=["Bitacora"])
def update_bitacora_entry(id_bitacora: int, entry: Bitacora, db: Session = Depends(get_db)):
    db.execute(bitacora.update().where(bitacora.c.id_bitacora == id_bitacora).values(entry.dict()))
    db.commit()
    return db.execute(bitacora.select().where(bitacora.c.id_bitacora == id_bitacora)).first()

# Eliminar una entrada de bitacora por ID
@bitacora_router.delete("/bitacora/{id_bitacora}", status_code=status.HTTP_204_NO_CONTENT, tags=["Bitacora"])
def delete_bitacora_entry(id_bitacora: int, db: Session = Depends(get_db)):
    db.execute(bitacora.delete().where(bitacora.c.id_bitacora == id_bitacora))
    db.commit()
    return {"message": "Bitacora entry deleted"}
