from pydantic import BaseModel

# ---------------------------------------------------------
# CU 1: Crear Pedido 
# ---------------------------------------------------------
class Pedido(BaseModel):
    id: int
    cliente: str
    direccion: str
    estado: str = "Creado" 

# ---------------------------------------------------------
# CU 2: Registrar Repartidor
# ---------------------------------------------------------
class Repartidor(BaseModel):
    id: int
    nombre: str
    disponible: bool = True

# ---------------------------------------------------------
# CU 3: Asignacion y Despacho
# ---------------------------------------------------------
class AsignacionRequest(BaseModel):
    repartidor_id: int

# ---------------------------------------------------------
# CU 4: Reportar Incidencia
# ---------------------------------------------------------
class Incidencia(BaseModel):
    id: int
    pedido_id: int
    descripcion: str
    gravedad: str