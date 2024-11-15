from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.db import SessionLocal  # Importamos la sesión local
from app.models.vehiculos_model import vehiculos
from app.schemas.vehiculos_schema import Vehiculo
from typing import List

# Instancia de APIRouter
vehiculos_router = APIRouter()

# Dependencia de sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los vehiculos
@vehiculos_router.get("/vehiculos", response_model=List[Vehiculo], tags=["Vehiculos"])
def get_vehiculos(db: Session = Depends(get_db)):
    return db.execute(vehiculos.select()).fetchall()

# Obtener un vehiculo por ID
@vehiculos_router.get("/vehiculos/{id_vehiculo}", response_model=Vehiculo, tags=["Vehiculos"])
def get_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
    vehiculo_found = db.execute(vehiculos.select().where(vehiculos.c.id_vehiculo == id_vehiculo)).first()
    if not vehiculo_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehiculo not found")
    return vehiculo_found

# Crear un nuevo vehiculo
@vehiculos_router.post("/vehiculos", response_model=Vehiculo, tags=["Vehiculos"])
def create_vehiculo(vehiculo_data: Vehiculo, db: Session = Depends(get_db)):
    result = db.execute(vehiculos.insert().values(vehiculo_data.dict()))
    db.commit()
    return db.execute(vehiculos.select().where(vehiculos.c.id_vehiculo == result.lastrowid)).first()

# Actualizar un vehiculo
@vehiculos_router.put("/vehiculos/{id_vehiculo}", response_model=Vehiculo, tags=["Vehiculos"])
def update_vehiculo(id_vehiculo: int, vehiculo_data: Vehiculo, db: Session = Depends(get_db)):
    db.execute(vehiculos.update().where(vehiculos.c.id_vehiculo == id_vehiculo).values(vehiculo_data.dict()))
    db.commit()
    return db.execute(vehiculos.select().where(vehiculos.c.id_vehiculo == id_vehiculo)).first()

# Eliminar un vehiculo por ID
@vehiculos_router.delete("/vehiculos/{id_vehiculo}", status_code=status.HTTP_204_NO_CONTENT, tags=["Vehiculos"])
def delete_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
    db.execute(vehiculos.delete().where(vehiculos.c.id_vehiculo == id_vehiculo))
    db.commit()
    return {"message": "Vehiculo deleted"}
