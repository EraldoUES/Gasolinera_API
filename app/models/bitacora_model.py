from sqlalchemy import Table, Column, Integer, Text, DECIMAL, ForeignKey
from app.config.db import meta, engine

#Tabla bitacora
bitacora = Table(
    'bitacora', meta,
    Column('id_bitacora', Integer, primary_key=True, autoincrement=True),
    Column('comentario', Text),
    Column('km_inicial', Integer),
    Column('km_final', Integer),
    Column('num_galones', DECIMAL(10, 2)),
    Column('costo', DECIMAL(10, 2)),
    Column('id_tipo_combustible', Integer, ForeignKey("tipo_combustible.id_tipo_combustible")),
    Column('id_usr', Integer, ForeignKey("usuarios.id_usr")),
    Column('id_vehiculo', Integer, ForeignKey("vehiculos.id_vehiculo")),
    Column('id_gasolinera', Integer, ForeignKey("gasolineras.id_gasolinera")),
    Column('id_proyecto', Integer, ForeignKey("proyecto.id_proyecto"))
)

meta.create_all(engine)
