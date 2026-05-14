from fastapi import HTTPException, status, Security, Depends
from fastapi.security import APIKeyHeader
from repositories.memory_db import usuarios_db

# Definimos los roles constantes
class Roles:
    ADMIN = "administrador"
    OPERADOR = "operador"
    REPARTIDOR = "repartidor"
    EXTERNO = "integracion_externa"

# 1. Definimos el esquema de seguridad basado en un token de usuario (en el Header)
# Esto hara que Swagger pida un "user-token" en lugar de un "rol"
token_scheme = APIKeyHeader(name="user-token", auto_error=True)

# 2. Función que busca el rol en la "BD" basándose en el token recibido
def obtener_rol_validado(token: str = Security(token_scheme)):
    rol = usuarios_db.get(token)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado: Token de usuario no válido o inexistente en la BD."
        )
    return rol

# 3. Dependencias de seguridad para los controladores
def solo_staff(rol: str = Depends(obtener_rol_validado)):
    if rol not in [Roles.ADMIN, Roles.OPERADOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acceso denegado: Se requiere perfil de Administrador u Operador"
        )
    return rol

def solo_admin(rol: str = Depends(obtener_rol_validado)):
    if rol != Roles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acceso denegado: Solo el Administrador puede registrar personal"
        )
    return rol

def solo_repartidor(rol: str = Depends(obtener_rol_validado)):
    if rol != Roles.REPARTIDOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acceso denegado: Solo un repartidor autenticado puede realizar esta acción"
        )
    return rol