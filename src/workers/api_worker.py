import asyncio
from PySide6.QtCore import QThread, Signal
from src.core.api_client import consultar_api_externa_async


class APIWorker(QThread):
    log_message = Signal(str)
    finished = Signal(dict)

    def run(self):
        self.log_message.emit("Iniciando petición asíncrona a la API externa (I/O Bound)...")
        self.log_message.emit("Esperando respuesta del servidor de fondo...")

        try:
            # Creamos un nuevo bucle de eventos de asyncio para este hilo secundario
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Ejecutamos la tarea asíncrona hasta que complete
            resultado = loop.run_until_complete(consultar_api_externa_async())
            loop.close()

            self.finished.emit({
                "status": "Success",
                "msg": "¡Sincronización con la API completada sin un solo milisegundo de lag!",
                "data": resultado
            })

        except Exception as e:
            self.log_message.emit(f"❌ Error en petición de red: {str(e)}")
            self.finished.emit({"status": "Error", "msg": str(e)})