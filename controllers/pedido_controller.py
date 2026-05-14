from fastapi import APIRouter, HTTPException, Depends # <-- Añadimos Depends
from models.schemas import Pedido, Repartidor, Incidencia, AsignacionRequest
from services.pedido_service import PedidoService
from security import solo_staff, solo_admin, solo_repartidor # <-- Importamos nuestras reglas

# Inicializamos el enrutador de FastAPI bajo el prefijo /api
router = APIRouter(prefix="/api")

# Instanciamos nuestra Capa de Servicio (Service Layer)
service = PedidoService()

# ---------------------------------------------------------
# CU 1: Gestión de Pedidos (Admin u Operador)
# ---------------------------------------------------------
@router.post("/pedidos", summary="CU 1: Crear Pedido")
def crear_pedido(pedido: Pedido, rol: str = Depends(solo_staff)):
    try:
        # El controlador delega el trabajo pesado al Servicio
        return service.gestionar_pedido(pedido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/pedidos/{pedido_id}", summary="CU 1: Consultar Pedido")
def consultar_pedido(pedido_id: int, rol: str = Depends(solo_staff)):
    pedido = service.repo.obtener_pedido(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

# ---------------------------------------------------------
# CU 2: Gestión de Repartidores (Solo Admin)
# ---------------------------------------------------------
@router.post("/repartidores", summary="CU 2: Registrar Repartidor")
def registrar_repartidor(repartidor: Repartidor, rol: str = Depends(solo_admin)):
    try:
        return service.gestionar_repartidor(repartidor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------------------------------------------------------
# CU 3: Asignación y Despacho (Admin u Operador)
# ---------------------------------------------------------
@router.put("/pedidos/{pedido_id}/asignar", summary="CU 3: Asignación y Despacho")
def asignar_pedido(pedido_id: int, request: AsignacionRequest, rol: str = Depends(solo_staff)):
    try:
        return service.asignar_despacho(pedido_id, request.repartidor_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------------------------------------------------------
# CU 4: Gestión de Incidencias (Solo Repartidor)
# ---------------------------------------------------------
@router.post("/incidencias", summary="CU 4: Reportar Incidencia")
def reportar_incidencia(incidencia: Incidencia, rol: str = Depends(solo_repartidor)):
    try:
        return service.gestionar_incidencia(incidencia)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------------------------------------------------------
# EXTRA: Finalizar ciclo (Solo Repartidor)
# ---------------------------------------------------------
@router.put("/pedidos/{pedido_id}/entregar", summary="Extra: Marcar Pedido como Entregado")
def entregar_pedido(pedido_id: int, rol: str = Depends(solo_repartidor)):
    try:
        return service.marcar_entregado(pedido_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))