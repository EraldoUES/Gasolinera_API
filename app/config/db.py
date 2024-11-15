from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import os

# URL de la base de datos
DATABASE_URL = "mariadb+pymysql://root:1234@localhost:3306/gestion_combustible"

# Configuración de la conexión
engine = create_engine(DATABASE_URL)
meta = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Llave de encriptación para las contraseñas
key = "QhShiRoHlkNYqAuZpzqcHWXY3bGf2sGgwSAf8LlN8zM="
