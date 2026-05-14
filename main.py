from fastapi import FastAPI
from controllers.pedido_controller import router
import uvicorn

# Inicializamos la aplicacion FastAPI. 
# Esta es la variable "app" exacta que Uvicorn estaba buscando.
app = FastAPI(
    title="Logística API - Entregable 2 UV",
    description="Servicio web para gestión de pedidos y repartidores",
    version="1.0.0"
)

# Conectamos las rutas (endpoints) que vienen desde el controlador
app.include_router(router)


# Motor para levantar el servidor si ejecutamos este archivo directamente
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)   