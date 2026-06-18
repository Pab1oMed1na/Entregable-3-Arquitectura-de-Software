from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from schemas import Repartidor, AsignacionRequest, Incidencia
from pedido_service import PedidoService

app = FastAPI(title="Servicio de Operaciones", port=8001)
pedido_service = PedidoService()

class EventoMock(BaseModel):
    tipo_evento: str
    pedido_id: int

# Consumidor de la cola asíncrona
@app.post("/eventos")
def consumir_evento(evento: EventoMock):
    if evento.tipo_evento == "PedidoCreado":
        print(f"\n[BROKER ASÍNCRONO] Alerta de Nuevo Pedido: El pedido ID {evento.pedido_id} está listo para ser despachado.\n")
    return {"status": "evento_procesado"}

@app.post("/repartidores")
def registrar_repartidor(repartidor: Repartidor):
    nuevo_repartidor = pedido_service.registrar_repartidor(repartidor)
    return {"mensaje": "Repartidor registrado", "repartidor": nuevo_repartidor}

@app.put("/pedidos/{pedido_id}/asignar")
def asignar_despacho(pedido_id: int, req: AsignacionRequest):
    resultado = pedido_service.asignar_despacho(pedido_id, req)
    if not resultado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"mensaje": f"Pedido {pedido_id} asignado al repartidor {req.repartidor_id}"}

@app.post("/incidencias")
def reportar_incidencia(incidencia: Incidencia):
    nueva_incidencia = pedido_service.reportar_incidencia(incidencia)
    return {"mensaje": "Incidencia reportada", "incidencia": nueva_incidencia}