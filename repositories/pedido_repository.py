from repositories.memory_db import pedidos_db, repartidores_db, incidencias_db
from models.schemas import Pedido, Repartidor, Incidencia

# Esta clase es la unica responsable de tocar los datos
class PedidoRepository:
    
    # Metodo para registrar un nuevo pedido en el diccionario de la memoria
    def guardar_pedido(self, pedido: Pedido):
        pedidos_db[pedido.id] = pedido
        return pedido

    # Metodo para buscar un pedido especifico por su identificador unico
    def obtener_pedido(self, pedido_id: int):
        return pedidos_db.get(pedido_id)

    # Metodo para registrar a un repartidor en el sistema
    def guardar_repartidor(self, repartidor: Repartidor):
        repartidores_db[repartidor.id] = repartidor
        return repartidor

    # Metodo para buscar a un repartidor por su ID
    def obtener_repartidor(self, repartidor_id: int):
        return repartidores_db.get(repartidor_id)

    # Metodo para registrar incidencias 
    def guardar_incidencia(self, incidencia: Incidencia):
        incidencias_db[incidencia.id] = incidencia
        return incidencia