from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    database_name: str = os.getenv("DATABASE_NAME", "ecommerce")
    app_name: str = os.getenv("APP_NAME", "E-commerce API")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", 8000))

    class Config:
        env_file = ".env"


settings = Settings()


class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def get_database():
    return db.database


async def connect_to_mongo():
    """Create database connection"""
    db.client = AsyncIOMotorClient(settings.mongodb_uri)
    db.database = db.client[settings.database_name]
    
    # Create indexes for better performance
    await db.database.products.create_index("name")
    await db.database.products.create_index("size")
    await db.database.products.create_index([("name", "text")])
    await db.database.orders.create_index("user_id")
    await db.database.orders.create_index("created_at")


async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
