# Entregable 2 — Servicio Web de Logística de Última Milla

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
pip install fastapi uvicorn pydantic
```

## Ejecución

```bash
uvicorn main:app --reload
```

El servicio queda disponible en `http://127.0.0.1:8000`.

Documentación interactiva (Swagger UI): `http://127.0.0.1:8000/docs`

## Estructura del proyecto

- `main.py` — Punto de entrada FastAPI
- `controllers/` — Endpoints HTTP (capa de exposición)
- `services/` — Lógica de negocio (Service Layer)
- `repositories/` — Acceso a datos (patrón Repository, en memoria)
- `models/` — DTOs/Schemas Pydantic
- `security.py` — Control de acceso basado en roles (RBAC)

## Casos de uso expuestos

| Método | Endpoint | CU | Rol requerido |
|--------|----------|----|---|
| POST | `/api/pedidos` | CU 1: Crear pedido | administrador / operador |
| GET  | `/api/pedidos/{id}` | CU 1: Consultar pedido | administrador / operador |
| POST | `/api/repartidores` | CU 2: Registrar repartidor | administrador |
| PUT  | `/api/pedidos/{id}/asignar` | CU 3: Asignar pedido | administrador / operador |
| POST | `/api/incidencias` | CU 4: Reportar incidencia | repartidor |
| PUT  | `/api/pedidos/{id}/entregar` | Extra: Marcar entregado | repartidor |

## Autenticación

Todos los endpoints requieren el header `rol` con uno de los valores: 
`administrador`, `operador`, `repartidor`, `integracion_externa`.

## Ejemplos de uso

Crear pedido:
```bash
curl -X POST http://127.0.0.1:8000/api/pedidos \
  -H "Content-Type: application/json" \
  -H "rol: administrador" \
  -d '{"id":1, "cliente":"Juan Pérez", "direccion":"Av. Brasil 1234"}'
```

Asignar pedido:
```bash
curl -X PUT http://127.0.0.1:8000/api/pedidos/1/asignar \
  -H "Content-Type: application/json" \
  -H "rol: operador" \
  -d '{"repartidor_id":1}'
```