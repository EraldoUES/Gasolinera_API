from sqlalchemy import Table, Column, Integer, String, DECIMAL, ForeignKey
from app.config.db import meta, engine

#Tabla Vehiculos
vehiculos = Table(
    'vehiculos', meta,
    Column('id_vehiculo', Integer, primary_key=True, autoincrement=True),
    Column('modelo', String(50)),
    Column('marca', String(50)),
    Column('placa', String(20), unique=True),
    Column('rendimiento', DECIMAL(10, 2)),
    Column('galonaje', DECIMAL(10, 2)),
    Column('id_tipo_combustible', Integer, ForeignKey("tipo_combustible.id_tipo_combustible"))
)

meta.create_all(engine)
