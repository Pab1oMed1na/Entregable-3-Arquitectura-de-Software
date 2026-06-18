from db_mock import obtener_conexion

class PedidoRepository:
    def crear_pedido(self, pedido_dict: dict):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pedidos (id, cliente, direccion, estado) VALUES (?, ?, ?, ?)",
            (pedido_dict["id"], pedido_dict["cliente"], pedido_dict["direccion"], pedido_dict.get("estado", "Creado"))
        )
        conn.commit()
        conn.close()
        return pedido_dict

    def registrar_repartidor(self, repartidor_dict: dict):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # Convertimos el booleano a 1 o 0 para SQLite
        disponible_int = 1 if repartidor_dict.get("disponible", True) else 0
        cursor.execute(
            "INSERT INTO repartidores (id, nombre, disponible) VALUES (?, ?, ?)",
            (repartidor_dict["id"], repartidor_dict["nombre"], disponible_int)
        )
        conn.commit()
        conn.close()
        return repartidor_dict

    def asignar_despacho(self, pedido_id: int, repartidor_id: int):
        conn = obtener_conexion()
        cursor = conn.cursor()
        nuevo_estado = f"Asignado al repartidor {repartidor_id}"
        
        cursor.execute(
            "UPDATE pedidos SET estado = ? WHERE id = ?",
            (nuevo_estado, pedido_id)
        )
        conn.commit()
        
        # Recuperamos el pedido actualizado para responderle correctamente a la API
        cursor.execute("SELECT id, cliente, direccion, estado FROM pedidos WHERE id = ?", (pedido_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {"id": row[0], "cliente": row[1], "direccion": row[2], "estado": row[3]}
        return None

    def reportar_incidencia(self, incidencia_dict: dict):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO incidencias (pedido_id, descripcion, gravedad) VALUES (?, ?, ?)",
            (incidencia_dict["pedido_id"], incidencia_dict["descripcion"], incidencia_dict["gravedad"])
        )
        conn.commit()
        conn.close()
        return incidencia_dict

    def listar_pedidos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, cliente, direccion, estado FROM pedidos")
        rows = cursor.fetchall()
        conn.close()
        
        # Transformamos los resultados de la BD en una lista de diccionarios
        pedidos = []
        for row in rows:
            pedidos.append({"id": row[0], "cliente": row[1], "direccion": row[2], "estado": row[3]})
        return pedidos