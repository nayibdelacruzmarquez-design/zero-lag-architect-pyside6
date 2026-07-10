import httpx


async def consultar_api_externa_async():
    """
    Simula una consulta asíncrona no bloqueante a una API externa lenta.
    Utiliza httpx para interactuar con el bucle de eventos sin congelar la UI.
    """
    url = "https://httpbin.org/delay/2"  # Simula un endpoint que tarda 2 segundos en responder

    async with httpx.AsyncClient(timeout=10.0) as client:
        # La ejecución se suspende aquí liberando el hilo, pero la UI sigue respondiendo
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(f"Error de red: Código de estado {response.status_code}")