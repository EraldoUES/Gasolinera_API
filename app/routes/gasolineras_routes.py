from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.db import SessionLocal  # Importamos la sesión local
from app.models.gasolineras_model import gasolineras
from app.schemas.gasolineras_schema import Gasolinera
from typing import List

# Instancia de APIRouter
gasolineras_router = APIRouter()

# Dependencia de sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todas las gasolineras
@gasolineras_router.get("/gasolineras", response_model=List[Gasolinera], tags=["Gasolineras"])
def get_gasolineras(db: Session = Depends(get_db)):
    return db.execute(gasolineras.select()).fetchall()

# Obtener una gasolinera por ID
@gasolineras_router.get("/gasolineras/{id_gasolinera}", response_model=Gasolinera, tags=["Gasolineras"])
def get_gasolinera(id_gasolinera: int, db: Session = Depends(get_db)):
    gasolinera_found = db.execute(gasolineras.select().where(gasolineras.c.id_gasolinera == id_gasolinera)).first()
    if not gasolinera_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gasolinera not found")
    return gasolinera_found

# Crear una nueva gasolinera
@gasolineras_router.post("/gasolineras", response_model=Gasolinera, tags=["Gasolineras"])
def create_gasolinera(gasolinera_data: Gasolinera, db: Session = Depends(get_db)):
    result = db.execute(gasolineras.insert().values(gasolinera_data.dict()))
    db.commit()
    return db.execute(gasolineras.select().where(gasolineras.c.id_gasolinera == result.lastrowid)).first()

# Actualizar una gasolinera
@gasolineras_router.put("/gasolineras/{id_gasolinera}", response_model=Gasolinera, tags=["Gasolineras"])
def update_gasolinera(id_gasolinera: int, gasolinera_data: Gasolinera, db: Session = Depends(get_db)):
    db.execute(gasolineras.update().where(gasolineras.c.id_gasolinera == id_gasolinera).values(gasolinera_data.dict()))
    db.commit()
    return db.execute(gasolineras.select().where(gasolineras.c.id_gasolinera == id_gasolinera)).first()

# Eliminar una gasolinera por ID
@gasolineras_router.delete("/gasolineras/{id_gasolinera}", status_code=status.HTTP_204_NO_CONTENT, tags=["Gasolineras"])
def delete_gasolinera(id_gasolinera: int, db: Session = Depends(get_db)):
    db.execute(gasolineras.delete().where(gasolineras.c.id_gasolinera == id_gasolinera))
    db.commit()
    return {"message": "Gasolinera deleted"}
