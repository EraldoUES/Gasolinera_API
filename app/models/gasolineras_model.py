from sqlalchemy import Table, Column, Integer, String
from app.config.db import meta, engine

#Tabla gasolineras
gasolineras = Table(
    'gasolineras', meta,
    Column('id_gasolinera', Integer, primary_key=True, autoincrement=True),
    Column('nombre', String(50)),
    Column('direccion', String(100))
)

meta.create_all(engine)
