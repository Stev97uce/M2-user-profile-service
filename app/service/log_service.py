import httpx
from app.models.user import SessionLog

async def create_log(log_data: dict):
    log = SessionLog(**log_data)
    
    # Enviar evento a Kafka para registrarlo en session-logger
    async with httpx.AsyncClient() as client:
        await client.post("http://session-logger:8000/log", json=log.dict())

    return log
