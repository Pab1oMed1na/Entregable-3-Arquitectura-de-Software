from fastapi import FastAPI, BackgroundTasks
from schemas import Pedido
from pedido_service import PedidoService

app = FastAPI(title="Servicio de Ventas", port=8000)
pedido_service = PedidoService()

@app.post("/pedidos")
async def crear_pedido(pedido: Pedido, background_tasks: BackgroundTasks):
    nuevo_pedido = pedido_service.crear_pedido(pedido)
    
    # Se dispara el evento asincrono sin bloquear al cliente
    background_tasks.add_task(pedido_service.simular_publicacion_evento, pedido.id)
    
    return {"mensaje": "Pedido creado exitosamente", "pedido": nuevo_pedido}

@app.get("/pedidos")
def listar_pedidos():
    pedidos = pedido_service.listar_pedidos()
    return {"pedidos": pedidos}