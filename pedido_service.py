from pedido_repository import PedidoRepository
import httpx
import asyncio

class PedidoService:
    def __init__(self):
        self.repository = PedidoRepository()

    def crear_pedido(self, pedido):
        return self.repository.crear_pedido(pedido.dict())

    def registrar_repartidor(self, repartidor):
        return self.repository.registrar_repartidor(repartidor.dict())

    def asignar_despacho(self, pedido_id: int, asignacion_req):
        return self.repository.asignar_despacho(pedido_id, asignacion_req.repartidor_id)

    def reportar_incidencia(self, incidencia):
        return self.repository.reportar_incidencia(incidencia.dict())

    # TECNOLOGÍA 2: Asincronía para el Entregable 3
    async def simular_publicacion_evento(self, pedido_id: int):
        await asyncio.sleep(1)  
        evento = {"tipo_evento": "PedidoCreado", "pedido_id": pedido_id}
        try:
            async with httpx.AsyncClient() as client:
                await client.post("http://127.0.0.1:8001/eventos", json=evento)
        except Exception as e:
            print(f"[ERROR COLA] No se pudo enviar el evento: {e}")

    def listar_pedidos(self):
        return self.repository.listar_pedidos()