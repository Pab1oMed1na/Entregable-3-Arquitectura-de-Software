# Entregable 3 

## Integrantes
- Cristóbal Soto
- Alonso Venegas
- Pablo Medina
- Ricardo Muñoz
- Simón Canales

## Requisitos
- Python 3.10+
- pip

## Instalación

```bash
pip install fastapi uvicorn pydantic httpx

## Cómo ejecutar el proyecto

El sistema está compuesto por dos microservicios independientes. Para ejecutarlos, asegúrese de tener Python instalado y abra **dos terminales separadas** en la carpeta raíz del proyecto.

**1. Levantar el Servicio de Ventas (Terminal 1)**
Este servicio atiende los requerimientos del cliente (Crear y Listar Pedidos).
\`\`\`bash
python -m uvicorn servicio_ventas:app --port 8000 --reload
\`\`\`

**2. Levantar el Servicio de Operaciones (Terminal 2)**
Este servicio gestiona la logística interna, los repartidores y reacciona a los eventos asíncronos.
\`\`\`bash
python -m uvicorn servicio_operaciones:app --port 8001 --reload
\`\`\`

*Nota: La base de datos SQLite (`base_datos.db`) se creará automáticamente en la carpeta al ejecutar la primera petición.*

## Cómo probar los Casos de Uso

Puede probar todos los endpoints a través de la interfaz Swagger UI generada por FastAPI:
* **Ventas:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Operaciones:** [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

**Flujo de prueba recomendado:**
1. Vaya al puerto 8000 y ejecute `POST /pedidos` para crear un pedido.
2. Observe la terminal del puerto 8001: verá un mensaje del Broker Asíncrono confirmando la recepción del evento de creación.
3. Vaya al puerto 8001 y registre un repartidor con `POST /repartidores`.
4. En el puerto 8001, asigne el pedido al repartidor usando `PUT /pedidos/{pedido_id}/asignar`.
5. Si lo requiere, reporte una incidencia en el puerto 8001 con `POST /incidencias`.
6. Vuelva al puerto 8000 y ejecute `GET /pedidos` para verificar que el estado del pedido se actualizó correctamente gracias a la persistencia compartida.

---

## Evidencia de Decisiones Tecnológicas

Tal como se detalla en la presentación, se implementaron dos tecnologías principales vistas en el curso para satisfacer los atributos de calidad exigidos:

### 1. Integración Asíncrona 
**Justificación:** Se requiere latencia baja de cara al cliente y alta disponibilidad. Si Ventas dependiera sincrónicamente de Operaciones, un fallo logístico impediría la captura de ventas.
**Evidencia en el código:**
* En `servicio_ventas.py` (líneas 12-14), se utiliza `BackgroundTasks` de FastAPI para despachar la notificación en segundo plano sin bloquear el hilo principal de la respuesta HTTP.
* En `pedido_service.py` (método `simular_publicacion_evento`), se utiliza `httpx.AsyncClient` para simular la publicación del evento `PedidoCreado` hacia el broker de Operaciones.
* En `servicio_operaciones.py` (endpoint `POST /eventos`), se actúa como consumidor de la cola de mensajería.

### 2. Persistencia Relacional (SQLite)
**Justificación:** El dominio exige consistencia e integridad referencial (por ejemplo, una incidencia no puede existir sin un pedido válido).
**Evidencia en el código:**
* En `db_mock.py`, se utiliza el motor nativo `sqlite3` para generar las tablas con relaciones estandarizadas, incluyendo llaves foráneas (`FOREIGN KEY (pedido_id) REFERENCES pedidos (id)`).
* En `pedido_repository.py`, se aísla la capa de acceso a datos utilizando sentencias SQL transaccionales (`INSERT`, `UPDATE`, `SELECT`), demostrando un bajo acoplamiento gracias al Patrón Repository.

