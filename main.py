from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import connect_to_mongo, close_mongo_connection, settings
from app.routes import router
import uvicorn

app = FastAPI(
    title=settings.app_name,
    description="A simple e-commerce API built with FastAPI and MongoDB",
    version="1.0.0",
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup"""
    await connect_to_mongo()
    print(f"Connected to MongoDB: {settings.database_name}")


@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    await close_mongo_connection()
    print("Disconnected from MongoDB")


@app.get("/")
async def root():
    return {
        "message": "Welcome to E-commerce API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", settings.port))
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=port,
        reload=settings.debug
    )
