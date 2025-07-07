from fastapi import FastAPI
from app.routes import users

app = FastAPI(
    title="User Profile Service",
    description="Registro y validación de usuarios para LavaNet",
    version="1.0.0"
)

app.include_router(users.router)
