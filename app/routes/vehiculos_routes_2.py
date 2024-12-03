from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.db import SessionLocal  # Importamos la sesión local
from app.models.vehiculos_model import vehiculos
from app.models.tipo_combustible_model import tipo_combustible
from app.models.user_model import usuarios
from app.schemas.vehiculos_schema import Vehiculo2  # Asegúrate de tener tu schema actualizado
from typing import List
from sqlalchemy import select

# Instancia de APIRouter
vehiculos_router2 = APIRouter()

# Dependencia de sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los vehículos con datos completos de las tablas relacionadas
@vehiculos_router2.get("/vehiculos2", response_model=List[Vehiculo2], tags=["Vehiculos"])
def get_vehiculos(db: Session = Depends(get_db)):
    query = select(
        vehiculos.c.id_vehiculo,
        vehiculos.c.modelo,
        vehiculos.c.marca,
        vehiculos.c.placa,
        vehiculos.c.rendimiento,
        vehiculos.c.galonaje,
        vehiculos.c.id_tipo_combustible,
        tipo_combustible.c.descripcion.label('descripcion_tipo_combustible')  # Campo adicional
    ).select_from(vehiculos).join(
        tipo_combustible, vehiculos.c.id_tipo_combustible == tipo_combustible.c.id_tipo_combustible
    )

    result = db.execute(query).fetchall()

    # Convertir el resultado a una lista de Vehiculo2 para el formato de respuesta
    return [
        Vehiculo2(
            id_vehiculo=row.id_vehiculo,
            modelo=row.modelo,
            marca=row.marca,
            placa=row.placa,
            rendimiento=row.rendimiento,
            galonaje=row.galonaje,
            id_tipo_combustible=row.id_tipo_combustible,
            descripcion=row.descripcion_tipo_combustible,  # Incluyendo el campo adicional
        )
        for row in result
    ]

# Obtener un vehículo específico por ID con datos completos de las tablas relacionadas
@vehiculos_router2.get("/vehiculos2/{id_vehiculo}", response_model=Vehiculo2, tags=["Vehiculos"])
def get_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
    query = select(
        vehiculos.c.id_vehiculo,
        vehiculos.c.modelo,
        vehiculos.c.marca,
        vehiculos.c.placa,
        vehiculos.c.rendimiento,
        vehiculos.c.galonaje,
        vehiculos.c.id_tipo_combustible,
        tipo_combustible.c.descripcion.label('descripcion_tipo_combustible')  # Campo adicional
    ).select_from(vehiculos).join(
        tipo_combustible, vehiculos.c.id_tipo_combustible == tipo_combustible.c.id_tipo_combustible
    ).where(vehiculos.c.id_vehiculo == id_vehiculo)

    vehiculo_entry = db.execute(query).first()
    if not vehiculo_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehiculo not found")

    return Vehiculo2(
        id_vehiculo=vehiculo_entry.id_vehiculo,
        modelo=vehiculo_entry.modelo,
        marca=vehiculo_entry.marca,
        placa=vehiculo_entry.placa,
        rendimiento=vehiculo_entry.rendimiento,
        galonaje=vehiculo_entry.galonaje,
        id_tipo_combustible=vehiculo_entry.id_tipo_combustible,
        descripcion=vehiculo_entry.descripcion_tipo_combustible,  # Incluyendo el campo adicional
    )

