from sqlalchemy import Table, Column, Integer, String, Boolean
from app.config.db import meta, engine

#Tabla proyecto
proyecto = Table(
    'proyecto', meta,
    Column('id_proyecto', Integer, primary_key=True, autoincrement=True),
    Column('nombre', String(50)),
    Column('direccion', String(100)),
    Column('activo', Boolean, default=True)
)

meta.create_all(engine)
