from sqlalchemy import Table, Column, Integer, String
from app.config.db import meta, engine

#Tabla tipo de combustible
tipo_combustible = Table(
    'tipo_combustible', meta,
    Column('id_tipo_combustible', Integer, primary_key=True, autoincrement=True),
    Column('descripcion', String(50), unique=True)
)

meta.create_all(engine)
