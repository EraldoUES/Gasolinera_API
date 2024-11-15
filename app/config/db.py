from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import os

# URL de la base de datos
DATABASE_URL = "postgresql://gestion_combustible_user:22kWQRk5sDQODSsRof5gFtJQKf5kHYqu@dpg-csrsqcjtq21c739p4oa0-a/gestion_combustible"

# Configuración de la conexión
engine = create_engine(DATABASE_URL)
meta = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Llave de encriptación para las contraseñas
key = "QhShiRoHlkNYqAuZpzqcHWXY3bGf2sGgwSAf8LlN8zM="
