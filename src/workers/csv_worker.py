import sys
from concurrent.futures import ProcessPoolExecutor
from PySide6.QtCore import QThread, Signal
from src.core.processor import procesar_bloque_masivo


class CSVWorker(QThread):
    # Señales seguras para comunicarse con el Main Thread (UI)
    progress = Signal(int)
    log_message = Signal(str)
    finished = Signal(dict)

    def __init__(self, ruta_csv):
        super().__init__()
        self.ruta_csv = ruta_csv
        self._is_cancelled = False

    def cancel(self):
        """Activa la bandera de cancelación segura."""
        self._is_cancelled = True

    def run(self):
        try:
            self.log_message.emit("Iniciando análisis forense del CSV (1M de registros)...")
            self.log_message.emit("Detectando núcleos de CPU disponibles para evadir el GIL...")

            total_chunks = 4
            resultados = []

            # Usamos ProcessPoolExecutor para paralelismo real en núcleos separados
            with ProcessPoolExecutor() as executor:
                futuros = []
                for idx in range(total_chunks):
                    if self._is_cancelled:
                        break
                    # Enviamos las tareas a los subprocesos del OS
                    f = executor.submit(procesar_bloque_masivo, self.ruta_csv, idx + 1, total_chunks)
                    futuros.append(f)

                # Monitoreo del progreso de los subprocesos de forma no bloqueante
                for num_paso in range(1, 101):
                    if self._is_cancelled:
                        executor.shutdown(wait=False, cancel_futures=True)
                        raise RuntimeWarning("Operación cancelada por el usuario.")

                    self.msleep(40)  # Mantiene el bucle de actualización fluido
                    self.progress.emit(num_paso)

                # Recolectar resultados de los procesos hijos
                for f in futuros:
                    if not self._is_cancelled:
                        resultados.append(f.result())

            if self._is_cancelled:
                raise RuntimeWarning("Operación cancelada por el usuario.")

            self.finished.emit({
                "status": "Success",
                "msg": f"¡Logro Oculto 'The Flash' desbloqueado! 1M de filas procesadas.",
                "details": resultados
            })

        except RuntimeWarning as rw:
            self.log_message.emit(f"⚠️ {str(rw)}")
            self.finished.emit({"status": "Cancelled", "msg": "Procesamiento abortado limpiamente."})
        except Exception as e:
            self.log_message.emit(f"❌ Error crítico en subproceso: {str(e)}")
            self.finished.emit({"status": "Error", "msg": str(e)})