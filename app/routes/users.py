from fastapi import APIRouter, HTTPException, Depends
from app.models.user import UserIn, UserOut
from app.db.mongo import db
from app.core.security import hash_password, verify_password
from app.service.log_service import create_log
import httpx
from typing import Optional
from datetime import datetime

router = APIRouter()

@router.post("/register")
async def register(user: UserIn, role_id: Optional[int] = None):
    existing_user = await db.users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    role = None
    if role_id:
        try:
            async with httpx.AsyncClient() as client:
                role_response = await client.get(
                    # Agregar el link de la ec2 del micro3
                    f"http://roles-permissions-service:8080/roles/{role_id}",
                    timeout=5.0
                )
                role_response.raise_for_status()
                role = role_response.json()
        except (httpx.HTTPError, httpx.TimeoutException):
            raise HTTPException(
                status_code=502,
                detail="No se pudo validar el rol con el servicio de roles"
            )

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["is_active"] = True
    if role:
        user_dict["role"] = role

    result = await db.users.insert_one(user_dict)

    await create_log({
        "username": user.username,
        "action": "register",
        "timestamp": datetime.utcnow(),
        "ip_address": request.client.host
    })

    return {"msg": "Usuario registrado exitosamente", "user_id": str(result.inserted_id)}

@router.post("/login", response_model=UserOut)
async def login(user: UserIn):
    db_user = await db.users.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    await create_log({
        "username": user.username,
        "action": "login",
        "timestamp": datetime.utcnow(),
        "ip_address": request.client.host
    })

    db_user["id"] = str(db_user["_id"])
    del db_user["_id"]
    del db_user["password"]

    return UserOut(**db_user)