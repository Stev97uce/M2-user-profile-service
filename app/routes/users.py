from fastapi import APIRouter, HTTPException
from app.models.user import UserIn, UserOut
from app.db.mongo import db
from app.core.security import hash_password, verify_password

router = APIRouter()

@router.post("/register")
async def register(user: UserIn):
    existing = await db.users.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["is_active"] = True
    await db.users.insert_one(user_dict)
    return {"msg": "Usuario registrado"}

@router.post("/login", response_model=UserOut)
async def login(user: UserIn):
    db_user = await db.users.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return UserOut(**db_user)
