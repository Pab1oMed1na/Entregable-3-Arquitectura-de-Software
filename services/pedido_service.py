from repositories.pedido_repository import PedidoRepository
from models.schemas import Pedido, Repartidor, Incidencia

class PedidoService:
    def __init__(self):
        # Instanciamos el repositorio. Gracias a este patrón, 
        # el servicio no sabe si usamos diccionarios, SQL o archivos.
        self.repo = PedidoRepository()

    # ---------------------------------------------------------
    # CU 1: Gestión de Pedidos
    # ---------------------------------------------------------
    def gestionar_pedido(self, pedido: Pedido):
        # 1. Validar que el ID no exista previamente en la "base de datos"
        if self.repo.obtener_pedido(pedido.id):
            raise ValueError("El pedido con este ID ya existe.")
        
        # 2. Validar reglas de negocio: El cliente no puede venir vacío
        if not pedido.cliente or not pedido.cliente.strip():
            raise ValueError("Error: El nombre del cliente no puede estar vacío.")
            
        # 3. Validar reglas de negocio: La dirección no puede venir vacía
        if not pedido.direccion or not pedido.direccion.strip():
            raise ValueError("Error: La dirección no puede estar vacía.")
            
        # 4. Regla estricta: Todo pedido nuevo nace obligatoriamente en estado "Creado"
        # (Así evitamos que nos manden un JSON diciendo que ya está "Entregado")
        pedido.estado = "Creado"
        
        # Guardamos usando el repositorio
        return self.repo.guardar_pedido(pedido)

    # ---------------------------------------------------------
    # CU 2: Gestión de Repartidores
    # ---------------------------------------------------------
    def gestionar_repartidor(self, repartidor: Repartidor):
        # 1. Evitar IDs duplicados
        if self.repo.obtener_repartidor(repartidor.id):
            raise ValueError("El repartidor con este ID ya está registrado.")
        
        # 2. Validar que el nombre sea real (no vacío y de más de 1 carácter)
        if not repartidor.nombre or len(repartidor.nombre.strip()) <= 1:
            raise ValueError("Error: El nombre del repartidor debe tener al menos 2 caracteres.")
            
        # 3. Regla de negocio: Un repartidor nuevo siempre entra disponible
        repartidor.disponible = True
        
        return self.repo.guardar_repartidor(repartidor)

    # ---------------------------------------------------------
    # CU 3: Asignación y Despacho
    # ---------------------------------------------------------
    def asignar_despacho(self, pedido_id: int, repartidor_id: int):
        # Verificamos que el pedido exista
        pedido = self.repo.obtener_pedido(pedido_id)
        if not pedido:
            raise ValueError("Error: El pedido no existe.")
        
        # Solo podemos asignar pedidos recien "Creados"
        if pedido.estado != "Creado":
            raise ValueError(f"Error: No se puede asignar un pedido que ya está en estado '{pedido.estado}'.")
        
        # Verificamos que el repartidor exista
        repartidor = self.repo.obtener_repartidor(repartidor_id)
        if not repartidor:
            raise ValueError("Error: El repartidor no existe.")
        
        # Verificamos que el repartidor no este ocupado con otro pedido
        if not repartidor.disponible:
            raise ValueError("Error de negocio: El repartidor no tiene capacidad o no está disponible.")
        
        # Efectuar la asignacion cambiando los estados de ambos
        pedido.estado = "Asignado"
        repartidor.disponible = False # Ahora queda ocupado
        
        # Guardamos los cambios de ambos objetos
        self.repo.guardar_pedido(pedido)
        self.repo.guardar_repartidor(repartidor)
        
        return {"mensaje": f"Pedido {pedido_id} asignado con éxito a {repartidor.nombre}"}

    # ---------------------------------------------------------
    # CU 4: Gestión de Incidencias
    # ---------------------------------------------------------
    def gestionar_incidencia(self, incidencia: Incidencia):
        # Validar que el pedido al que le vamos a clavar la incidencia exista
        pedido = self.repo.obtener_pedido(incidencia.pedido_id)
        if not pedido:
            raise ValueError("Error: No se puede reportar incidencia. El pedido asociado no existe.")
        
        # Coherencia de negocio: Un paquete no puede chocar si sigue en la bodega
        # Tampoco si ya fue "Entregado" con exito. Solo si esta "Asignado" o "En Camino".
        if pedido.estado not in ["Asignado", "En Camino"]:
            raise ValueError(f"Error lógico: No se puede reportar una incidencia si el pedido está '{pedido.estado}'. Debe estar 'Asignado' o 'En Camino'.")
        
        # Tipos de gravedad permitidos por el dominio
        if incidencia.gravedad not in ["Alta", "Media", "Baja"]:
            raise ValueError("Error: La gravedad de la incidencia debe ser estrictamente 'Alta', 'Media' o 'Baja'.")
        
        # Cambiamos el estado del pedido para reflejar el problema
        pedido.estado = "Con Incidencia"
        self.repo.guardar_pedido(pedido)
        
        return self.repo.guardar_incidencia(incidencia)
        
    # ---------------------------------------------------------
    # EXTRA: Finalizar ciclo (Marcar como Entregado)
    # ---------------------------------------------------------
    def marcar_entregado(self, pedido_id: int):
        # 1. Validar que el pedido exista
        pedido = self.repo.obtener_pedido(pedido_id)
        if not pedido:
            raise ValueError("Error: El pedido no existe.")
        
        # 2. Lógica de negocio: Solo se entrega si estaba en ruta o asignado
        if pedido.estado not in ["Asignado", "En Camino"]:
            raise ValueError(f"Error: No se puede entregar un pedido que está en estado '{pedido.estado}'.")
        
        # 3. Cerramos el ciclo
        pedido.estado = "Entregado"
        return self.repo.guardar_pedido(pedido)