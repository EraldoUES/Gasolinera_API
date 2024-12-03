from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.db import SessionLocal, key
from app.models.user_model import usuarios
from app.models.rol_model import rol
from app.schemas.user_schema import LoginRequest, User
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
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    username = login_request.username
    password = login_request.password

    print(f"Recibiendo solicitud de login para el usuario: {username}")

    # Buscar usuario por nombre de usuario
    db_user = db.execute(usuarios.select().where(usuarios.c.username == username)).fetchone()
    
    # Verificar si se encontró el usuario
    if not db_user:
        print(f"Usuario no encontrado: {username}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Verificar si db_user es un Row, y acceder por el nombre de la columna
    print(f"Usuario encontrado: {db_user}")
    stored_password = db_user.password  # Asegúrate de acceder por nombre de columna

    try:
        # Desencriptar y verificar la contraseña
        decrypted_password = fernet.decrypt(stored_password.encode('utf-8')).decode()
        print(f"Contraseña desencriptada: {decrypted_password}")
        if decrypted_password != password:
            # Registrar intento fallido
            print(f"Contraseña incorrecta para el usuario: {username}")
            registrar_login_usuario(db, username, login_exitoso=False)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    except Exception as e:
        # Error al desencriptar
        print(f"Error al desencriptar la contraseña para el usuario {username}: {e}")
        registrar_login_usuario(db, username, login_exitoso=False)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    # Registrar intento exitoso
    print(f"Login exitoso para el usuario: {username}")
    registrar_login_usuario(db, username, login_exitoso=True)
    
    # Obtener el rol del usuario
    user_role = db.execute(rol.select().where(rol.c.id_rol == db_user.id_rol)).first()
    print(f"Rol del usuario obtenido: {user_role}")

    # Si no se encuentra el rol
    if not user_role:
        print(f"Rol no encontrado para el usuario: {username}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    # Verificar el rol del usuario
    if user_role.descripcion.lower() == "administrador":
        print(f"Rol de administrador detectado para el usuario: {username}")
        return {"message": "Login successful", "role": "admin","username": str(username),"id": str(db_user.id_usr)}
    else:
        print(f"Rol de usuario detectado para el usuario: {username}")
        return {"message": "Login successful", "role": "user","username": str(username),"id": str(db_user.id_usr)}



# Función para registrar el intento de login
def registrar_login_usuario(db: Session, username: str, login_exitoso: bool):
    try:
        # Usar `text()` para envolver la consulta SQL
        db.execute(text("CALL gestion_combustible_login(:username, :login_exitoso)"),{'username': username, 'login_exitoso': login_exitoso})
        db.commit()
    except Exception as ex:
        # Si hay un error, lanzar una excepción HTTP con detalles
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al registrar login: {str(ex)}")

