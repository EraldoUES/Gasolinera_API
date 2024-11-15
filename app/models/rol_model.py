from sqlalchemy import Table, Column, Integer, String
from app.config.db import meta, engine

#Tabla rol
rol = Table(
    'rol', meta,
    Column('id_rol', Integer, primary_key=True, autoincrement=True),
    Column('descripcion', String(50))
)

meta.create_all(engine)
