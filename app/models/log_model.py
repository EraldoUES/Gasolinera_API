from sqlalchemy import Table, Column, Integer, Text, TIMESTAMP, ForeignKey
from app.config.db import meta, engine

#Tabla log
log = Table(
    'log', meta,
    Column('id_log', Integer, primary_key=True, autoincrement=True),
    Column('descripcion', Text),
    Column('id_usr', Integer, ForeignKey("usuarios.id_usr")),
    Column('fecha', TIMESTAMP, default="CURRENT_TIMESTAMP")
)

meta.create_all(engine)
