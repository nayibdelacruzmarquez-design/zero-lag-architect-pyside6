import time


def procesar_bloque_masivo(ruta_csv, chunk_id, total_chunks):
    """
    Función pura que simula el parseo y cálculo matemático pesado de un fragmento del CSV.
    Al ejecutarse en un ProcessPoolExecutor, corre en un núcleo de CPU separado,
    liberando al 100% el Main Thread de la UI.
    """
    # Simulamos el procesamiento de un lote pesado (ej. 250,000 registros por núcleo)
    registros_por_chunk = 250000

    for i in range(1, 101):
        # Simulación de carga matemática pesada por cada 1% de avance del fragmento
        _ = [x ** 2 for x in range(5000)]  # Estrés de CPU
        time.sleep(0.01)  # Simula latencia de procesamiento de disco/cómputo

    return f"Chunk {chunk_id} procesado con éxito ({registros_por_chunk} filas)."