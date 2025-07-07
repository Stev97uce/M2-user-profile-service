import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")  
DB_NAME = os.getenv("DB_NAME", "lavanet")  

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000 
    )
    db = client[DB_NAME]
    print("✅ Conexión a MongoDB establecida")
except Exception as e:
    print(f"❌ Error conectando a MongoDB: {e}")
    raise