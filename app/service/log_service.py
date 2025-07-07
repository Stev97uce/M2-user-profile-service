import httpx
import os
from app.models.user import SessionLog

async def create_log(log_data: dict):
    log = SessionLog(**log_data)
    session_logger_url = os.getenv("SESSION_LOGGER_URL") 
    
    async with httpx.AsyncClient() as client:
        try:
            await client.post(f"{session_logger_url}/log", json=log.dict())
        except httpx.RequestError as e:
            print(f"Error calling session-logger: {e}") 

    return log