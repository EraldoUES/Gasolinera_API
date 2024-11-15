from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.db import SessionLocal  # Importamos la sesión local
from app.models.log_model import log
from app.schemas.log_schema import Log
from typing import List

# Instancia de APIRouter
log_router = APIRouter()

# Dependencia de sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los logs
@log_router.get("/logs", response_model=List[Log], tags=["Logs"])
def get_logs(db: Session = Depends(get_db)):
    return db.execute(log.select()).fetchall()

# Obtener un log por ID
@log_router.get("/logs/{id_log}", response_model=Log, tags=["Logs"])
def get_log(id_log: int, db: Session = Depends(get_db)):
    log_found = db.execute(log.select().where(log.c.id_log == id_log)).first()
    if not log_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log entry not found")
    return log_found

# Crear una nueva entrada de log
@log_router.post("/logs", response_model=Log, tags=["Logs"])
def create_log(log_data: Log, db: Session = Depends(get_db)):
    result = db.execute(log.insert().values(log_data.dict()))
    db.commit()
    return db.execute(log.select().where(log.c.id_log == result.lastrowid)).first()

# Eliminar un log por ID
@log_router.delete("/logs/{id_log}", status_code=status.HTTP_204_NO_CONTENT, tags=["Logs"])
def delete_log(id_log: int, db: Session = Depends(get_db)):
    db.execute(log.delete().where(log.c.id_log == id_log))
    db.commit()
    return {"message": "Log entry deleted"}
