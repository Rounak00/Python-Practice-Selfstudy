import motor.motor_asyncio
from beanie import init_beanie
from app.models.todo_model import Todo
from dotenv import load_dotenv
import os

load_dotenv()

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL"))
    db = client[os.getenv("MONGO_DB_NAME")]

    await init_beanie(database=db, document_models=[Todo])
    print("✅ MongoDB connected successfully!")
