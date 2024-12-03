from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.db import SessionLocal  # Importamos la sesión local
from app.models.bitacora_model import bitacora
from app.models.gasolineras_model import gasolineras
from app.models.user_model import usuarios
from app.models.vehiculos_model import vehiculos
from app.models.proyecto_model import proyecto
from app.models.tipo_combustible_model import tipo_combustible
from app.schemas.bitacora_schema import Bitacora4, Bitacora3,User, Gasolinera, TipoCombustible, Proyecto, Vehiculo
from typing import List
from sqlalchemy import select


# Instancia de APIRouter
bitacora_router2 = APIRouter()

# Dependencia de sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@bitacora_router2.get("/data", response_model=Bitacora4, tags=["Data"])
def get_all_data(db: Session = Depends(get_db)):
    # Consultas para obtener todos los usuarios, gasolineras, tipos de combustible, proyectos y vehículos
    query_users = select(usuarios.c.id_usr, usuarios.c.username)
    query_gasolineras = select(gasolineras.c.id_gasolinera, gasolineras.c.nombre)
    query_tipos_combustible = select(tipo_combustible.c.id_tipo_combustible, tipo_combustible.c.descripcion)
    query_proyectos = select(proyecto.c.id_proyecto, proyecto.c.nombre)
    query_vehiculos = select(vehiculos.c.id_vehiculo, vehiculos.c.placa)

    # Ejecutar las consultas
    result_users = db.execute(query_users).fetchall()
    result_gasolineras = db.execute(query_gasolineras).fetchall()
    result_tipos_combustible = db.execute(query_tipos_combustible).fetchall()
    result_proyectos = db.execute(query_proyectos).fetchall()
    result_vehiculos = db.execute(query_vehiculos).fetchall()

    # Formatear los resultados en las clases correspondientes
    users1 = [User(id_usr=row.id_usr, username=row.username) for row in result_users]
    gasolineras1 = [Gasolinera(id_gasolinera=row.id_gasolinera, nombre_gasolinera=row.nombre) for row in result_gasolineras]
    tipos_combustible1 = [TipoCombustible(id_tipo_combustible=row.id_tipo_combustible, descripcion_tipo_combustible=row.descripcion) for row in result_tipos_combustible]
    proyectos1 = [Proyecto(id_proyecto=row.id_proyecto, nombre_proyecto=row.nombre) for row in result_proyectos]
    vehiculos1 = [Vehiculo(id_vehiculo=row.id_vehiculo, placa_vehiculo=row.placa) for row in result_vehiculos]

    # Devolver los datos en el formato esperado por el esquema Bitacora4
    return Bitacora4(
        users=users1,
        gasolineras=gasolineras1,
        tipos_combustible=tipos_combustible1,
        proyectos=proyectos1,
        vehiculos=vehiculos1
    )


# Obtener todas las entradas de bitacora con los datos completos de las tablas relacionadas
@bitacora_router2.get("/bitacora2", response_model=List[Bitacora3], tags=["Bitacora"])
def get_bitacora_entries(db: Session = Depends(get_db)):
    query = select(
        bitacora.c.id_bitacora,
        bitacora.c.comentario,
        bitacora.c.km_inicial,
        bitacora.c.km_final,
        bitacora.c.num_galones,
        bitacora.c.costo,
        bitacora.c.id_tipo_combustible,
        tipo_combustible.c.descripcion.label('descripcion_tipo_combustible'),
        bitacora.c.id_usr,
        usuarios.c.username,
        bitacora.c.id_vehiculo,
        vehiculos.c.placa.label('placa_vehiculo'),
        bitacora.c.id_gasolinera,
        gasolineras.c.nombre.label('nombre_gasolinera'),
        bitacora.c.id_proyecto,
        proyecto.c.nombre.label('nombre_proyecto')
    ).select_from(bitacora).join(
        tipo_combustible, bitacora.c.id_tipo_combustible == tipo_combustible.c.id_tipo_combustible
    ).join(
        usuarios, bitacora.c.id_usr == usuarios.c.id_usr
    ).join(
        vehiculos, bitacora.c.id_vehiculo == vehiculos.c.id_vehiculo
    ).join(
        gasolineras, bitacora.c.id_gasolinera == gasolineras.c.id_gasolinera
    ).join(
        proyecto, bitacora.c.id_proyecto == proyecto.c.id_proyecto
    )

    result = db.execute(query).fetchall()
    # Convertir el resultado a una lista de Bitacora3 para el formato de respuesta
    return [
        Bitacora3(
            id_bitacora=row.id_bitacora,
            comentario=row.comentario,
            km_inicial=row.km_inicial,
            km_final=row.km_final,
            num_galones=row.num_galones,
            costo=row.costo,
            id_tipo_combustible=row.id_tipo_combustible,
            descripcion_tipo_combustible=row.descripcion_tipo_combustible,
            id_usr=row.id_usr,
            username=row.username,
            id_vehiculo=row.id_vehiculo,
            placa_vehiculo=row.placa_vehiculo,
            id_gasolinera=row.id_gasolinera,
            nombre_gasolinera=row.nombre_gasolinera,
            id_proyecto=row.id_proyecto,
            nombre_proyecto=row.nombre_proyecto,
        )
        for row in result
    ]


# Obtener una entrada específica de bitacora por ID con los datos completos de las tablas relacionadas
@bitacora_router2.get("/bitacora2/{id_bitacora}", response_model=Bitacora3, tags=["Bitacora"])
def get_bitacora_entry(id_bitacora: int, db: Session = Depends(get_db)):
    query = select(
        bitacora.c.id_bitacora,
        bitacora.c.comentario,
        bitacora.c.km_inicial,
        bitacora.c.km_final,
        bitacora.c.num_galones,
        bitacora.c.costo,
        bitacora.c.id_tipo_combustible,
        tipo_combustible.c.descripcion.label('descripcion_tipo_combustible'),
        bitacora.c.id_usr,
        usuarios.c.username,
        bitacora.c.id_vehiculo,
        vehiculos.c.placa.label('placa_vehiculo'),
        bitacora.c.id_gasolinera,
        gasolineras.c.nombre.label('nombre_gasolinera'),
        bitacora.c.id_proyecto,
        proyecto.c.nombre.label('nombre_proyecto')
    ).select_from(bitacora).join(
        tipo_combustible, bitacora.c.id_tipo_combustible == tipo_combustible.c.id_tipo_combustible
    ).join(
        usuarios, bitacora.c.id_usr == usuarios.c.id_usr
    ).join(
        vehiculos, bitacora.c.id_vehiculo == vehiculos.c.id_vehiculo
    ).join(
        gasolineras, bitacora.c.id_gasolinera == gasolineras.c.id_gasolinera
    ).join(
        proyecto, bitacora.c.id_proyecto == proyecto.c.id_proyecto
    ).where(
        bitacora.c.id_bitacora == id_bitacora
    )

    bitacora_entry = db.execute(query).first()
    if not bitacora_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bitacora entry not found")

    return Bitacora3(
        id_bitacora=bitacora_entry.id_bitacora,
        comentario=bitacora_entry.comentario,
        km_inicial=bitacora_entry.km_inicial,
        km_final=bitacora_entry.km_final,
        num_galones=bitacora_entry.num_galones,
        costo=bitacora_entry.costo,
        id_tipo_combustible=bitacora_entry.id_tipo_combustible,
        descripcion_tipo_combustible=bitacora_entry.descripcion_tipo_combustible,
        id_usr=bitacora_entry.id_usr,
        username=bitacora_entry.username,
        id_vehiculo=bitacora_entry.id_vehiculo,
        placa_vehiculo=bitacora_entry.placa_vehiculo,
        id_gasolinera=bitacora_entry.id_gasolinera,
        nombre_gasolinera=bitacora_entry.nombre_gasolinera,
        id_proyecto=bitacora_entry.id_proyecto,
        nombre_proyecto=bitacora_entry.nombre_proyecto,
    )
