from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from app.config.db import SessionLocal, key
from app.models.user_model import usuarios
from app.models.rol_model import rol
from app.schemas.user_schema import User5, User2, User3, User4
from typing import List, Optional
from cryptography.fernet import Fernet
from pydantic import BaseModel

# Instancia APIRouter
user2 = APIRouter()

fernet = Fernet(key)

# Dependencia de sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los usuarios con su rol
@user2.get("/users2", response_model=List[User2], tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    query = (
        select(
            usuarios.c.id_usr,
            usuarios.c.nombre,
            usuarios.c.apellido,
            usuarios.c.username,
            usuarios.c.id_rol,
            usuarios.c.activo,
            rol.c.descripcion.label("rol")
        )
        .select_from(usuarios.outerjoin(rol, usuarios.c.id_rol == rol.c.id_rol))
    )
    results = db.execute(query).fetchall()
    return [dict(row._mapping) for row in results]

# Obtener un usuario por ID con su rol
@user2.get("/users2.id/{id_usr}", response_model=User2, tags=["Users"])
def get_user(id_usr: int, db: Session = Depends(get_db)):
    query = (
        select(
            usuarios.c.id_usr,
            usuarios.c.nombre,
            usuarios.c.apellido,
            usuarios.c.username,
            usuarios.c.id_rol,
            usuarios.c.activo,
            rol.c.descripcion.label("rol")
        )
        .select_from(usuarios.outerjoin(rol, usuarios.c.id_rol == rol.c.id_rol))
        .where(usuarios.c.id_usr == id_usr)
    )
    result = db.execute(query).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return dict(result._mapping)

@user2.get("/users2.name/{username}", response_model=User2, tags=["Users"])
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    query = (
        select(
            usuarios.c.id_usr,
            usuarios.c.nombre,
            usuarios.c.apellido,
            usuarios.c.username,
            usuarios.c.activo,
            rol.c.descripcion.label("rol"),
            usuarios.c.id_rol  # Agrega el campo id_rol
        )
        .select_from(usuarios.outerjoin(rol, usuarios.c.id_rol == rol.c.id_rol))
        .where(usuarios.c.username == username)
    )
    result = db.execute(query).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Convertir la fila en un diccionario
    return dict(result._mapping)

# Actualizar un usuario (sin modificar la contraseña)
@user2.put("/users2/{id_usr}", response_model=User3, tags=["Users"])
def update_user(id_usr: int, user3: User3, db: Session = Depends(get_db)):
    current_user = db.execute(select(usuarios).where(usuarios.c.id_usr == id_usr)).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_values = {
        "nombre": user3.nombre,
        "apellido": user3.apellido,
        "username": user3.username,
        "id_rol": user3.id_rol,
        "activo": user3.activo,
    }

    db.execute(usuarios.update().where(usuarios.c.id_usr == id_usr).values(**update_values))
    db.commit()

    query = (
        select(
            usuarios.c.id_usr,
            usuarios.c.nombre,
            usuarios.c.apellido,
            usuarios.c.username,
            usuarios.c.id_rol,
            usuarios.c.activo,
            rol.c.descripcion.label("rol")
        )
        .select_from(usuarios.outerjoin(rol, usuarios.c.id_rol == rol.c.id_rol))
        .where(usuarios.c.id_usr == id_usr)
    )
    result = db.execute(query).first()
    return dict(result._mapping)

# Actualizar un usuario con contraseña (obligatoria)
@user2.put("/users2/{id_usr}/password", response_model=User4, tags=["Users"])
def update_user_with_password(id_usr: int, user3: User4, db: Session = Depends(get_db)):
    # Encriptar la contraseña proporcionada
    encrypted_password = fernet.encrypt(user3.password.encode("utf-8")).decode()
    
    # Realizar la actualización en la base de datos
    db.execute(usuarios.update().where(usuarios.c.id_usr == id_usr).values(
        nombre=user3.nombre,
        apellido=user3.apellido,
        username=user3.username,
        password=encrypted_password,  # Contraseña encriptada
        id_rol=user3.id_rol,
        activo=user3.activo
    ))
    db.commit()

    # Obtener el usuario actualizado y su rol
    query = (
        select(
            usuarios.c.id_usr,
            usuarios.c.nombre,
            usuarios.c.apellido,
            usuarios.c.username,
            usuarios.c.id_rol,
            usuarios.c.activo,
            rol.c.descripcion.label("rol")
        )
        .select_from(usuarios.outerjoin(rol, usuarios.c.id_rol == rol.c.id_rol))
        .where(usuarios.c.id_usr == id_usr)
    )
    result = db.execute(query).first()
    
    # Devuelve el usuario actualizado con su rol
    return dict(result._mapping)

# Eliminar un usuario
@user2.delete("/users2/{id_usr}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"]) 
def delete_user(id_usr: int, db: Session = Depends(get_db)):
    # Verificar si el usuario existe
    user_to_delete = db.execute(select(usuarios).where(usuarios.c.id_usr == id_usr)).first()
    
    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Eliminar el usuario
    db.execute(usuarios.delete().where(usuarios.c.id_usr == id_usr))
    db.commit()

    return {"message": "User deleted"}

# Crear un nuevo usuario
@user2.post("/users2", response_model=User5, tags=["Users"])
def create_user(user: User5, db: Session = Depends(get_db)):
    try:
        # Validar entrada
        if not user.nombre or not user.apellido or not user.username or not user.password:
            raise HTTPException(status_code=400, detail="Todos los campos son obligatorios.")

        # Encriptar la contraseña
        encrypted_password = fernet.encrypt(user.password.encode("utf-8")).decode()

        # Crear nuevo usuario
        new_user = {
            "nombre": user.nombre,
            "apellido": user.apellido,
            "username": user.username,
            "password": encrypted_password,
            "id_rol": user.id_rol,
            "activo": user.activo
        }
        result = db.execute(usuarios.insert().values(new_user))
        db.commit()

        # Consultar y devolver el usuario recién creado
        created_user = db.execute(
            usuarios.select().where(usuarios.c.id_usr == result.lastrowid)
        ).first()

        if not created_user:
            raise HTTPException(status_code=500, detail="Error al crear el usuario.")
        
        return {
            "id_usr": created_user.id_usr,
            "nombre": created_user.nombre,
            "apellido": created_user.apellido,
            "username": created_user.username,
            "password": "*****",
            "id_rol": created_user.id_rol,
            "activo": created_user.activo
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
