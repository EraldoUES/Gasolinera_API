from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.config.db import SessionLocal  # Importamos la sesión local
from app.models.log_model import log
from app.models.user_model import usuarios
from app.schemas.log_schema import Log, Log2
from typing import List
from sqlalchemy import select

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

# Obtener todos los logs con datos completos de usuarios
@log_router.get("/logs2", response_model=List[Log2], tags=["Logs"])
def get_logs(db: Session = Depends(get_db)):
    query = select(
        log.c.id_log,
        log.c.descripcion,
        log.c.id_usr,
        usuarios.c.username,
        log.c.fecha
    ).select_from(log).join(
        usuarios, log.c.id_usr == usuarios.c.id_usr
    )

    result = db.execute(query).fetchall()
    return [
        Log2(
            id_log=row.id_log,
            descripcion=row.descripcion,
            id_usr=row.id_usr,
            username=row.username,
            fecha=row.fecha,
        )
        for row in result
    ]

# Obtener un log específico por ID con datos completos de las tablas relacionadas
@log_router.get("/logs2/{id_log}", response_model=Log2, tags=["Logs"])
def get_log(id_log: int, db: Session = Depends(get_db)):
    query = select(
        log.c.id_log,
        log.c.descripcion,
        log.c.id_usr,
        usuarios.c.username.label("username"),  # Nombre de usuario relacionado
        log.c.fecha
    ).select_from(log).join(
        usuarios, log.c.id_usr == usuarios.c.id_usr
    ).where(
        log.c.id_log == id_log
    )

    log_entry = db.execute(query).first()
    if not log_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log entry not found")

    # Convertir el resultado en una instancia de Log2
    return Log2(
        id_log=log_entry.id_log,
        descripcion=log_entry.descripcion,
        id_usr=log_entry.id_usr,
        username=log_entry.username,
        fecha=log_entry.fecha,
    )
