from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.db import SessionLocal, key
from app.models.user_model import usuarios
from app.schemas.user_schema import User
from typing import List
from cryptography.fernet import Fernet
from sqlalchemy import text

# Instancia APIRouter
user = APIRouter()

fernet = Fernet(key)

# Dependencia de sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Obtener todos los usuarios
@user.get("/users", response_model=List[User], tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    return db.execute(usuarios.select()).fetchall()

# Obtener un usuario por ID
@user.get("/users.id/{id_usr}", response_model=User, tags=["Users"])
def get_user(id_usr: int, db: Session = Depends(get_db)):
    user = db.execute(usuarios.select().where(usuarios.c.id_usr == id_usr)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Obtener un usuario por username
@user.get("/users.name/{username}", response_model=User, tags=["Users"])
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.execute(usuarios.select().where(usuarios.c.username == username)).fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Crear un nuevo usuario
@user.post("/users", response_model=User, tags=["Users"])
def create_user(user: User, db: Session = Depends(get_db)):
    encrypted_password = fernet.encrypt(user.password.encode("utf-8")).decode()
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
    return db.execute(usuarios.select().where(usuarios.c.id_usr == result.lastrowid)).first()

# Actualizar un usuario
@user.put("/users/{id_usr}", response_model=User, tags=["Users"])
def update_user(id_usr: int, user: User, db: Session = Depends(get_db)):
    encrypted_password = fernet.encrypt(user.password.encode("utf-8")).decode()
    db.execute(usuarios.update().where(usuarios.c.id_usr == id_usr).values(
        nombre=user.nombre,
        apellido=user.apellido,
        username=user.username,
        password=encrypted_password,
        id_rol=user.id_rol,
        activo=user.activo
    ))
    db.commit()
    return db.execute(usuarios.select().where(usuarios.c.id_usr == id_usr)).first()

# Eliminar un usuario
@user.delete("/users/{id_usr}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id_usr: int, db: Session = Depends(get_db)):
    db.execute(usuarios.delete().where(usuarios.c.id_usr == id_usr))
    db.commit()
    return {"message": "User deleted"}


# Ruta para login
@user.post("/login", tags=["Users"])
def login(username: str, password: str, db: Session = Depends(get_db)):
    # Buscar el usuario en la base de datos por el nombre de usuario
    db_user = db.execute(usuarios.select().where(usuarios.c.username == username)).fetchone()
    
    # Verificar si el usuario existe y si la contraseña es correcta
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Desencriptar la contraseña almacenada
    stored_password = db_user.password
    if fernet.decrypt(stored_password.encode('utf-8')).decode() != password:
        # Si la contraseña no coincide, se registra el intento de login fallido en la base de datos
        registrar_login_usuario(db, username, login_exitoso=False)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    # Si el login es exitoso, registrar el intento en la base de datos
    registrar_login_usuario(db, username, login_exitoso=True)
    
    return {"message": "Login successful"}

# Función para registrar el intento de login
def registrar_login_usuario(db: Session, username: str, login_exitoso: bool):
    # Usar `text()` para envolver la consulta SQL
    db.execute(text("CALL gestion_combustible_login(:username, :login_exitoso)"), 
               {'username': username, 'login_exitoso': login_exitoso})
    db.commit()
