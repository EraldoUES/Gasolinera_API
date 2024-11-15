from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from app.config.db import meta

#Tabla Usuarios
usuarios = Table(
    'usuarios', meta,
    Column('id_usr', Integer, primary_key=True, autoincrement=True),
    Column('nombre', String(50)),
    Column('apellido', String(50)),
    Column('password', String(255)),
    Column('username', String(50), unique=True),
    Column('id_rol', Integer, ForeignKey("rol.id_rol")),
    Column('activo', Boolean, default=True)
)
