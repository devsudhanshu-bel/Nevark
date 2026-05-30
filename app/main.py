from fastapi import FastAPI

from app.api.router import api_router

from app.database.database import engine
from app.database.models import Base

from app.utils.logger import logger

# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(bind=engine)

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(

    title="Nevark AI Backend",

    version="1.0.0"
)

# ============================================================
# INCLUDE ROUTES
# ============================================================

app.include_router(api_router)

# ============================================================
# ROOT ROUTE
# ============================================================

@app.get("/")
async def root():

    return {

        "message": "Nevark AI Backend Running",

        "status": "online"
    }

# ============================================================
# STARTUP EVENT
# ============================================================

@app.on_event("startup")
async def startup_event():

    logger.info(
        "🚀 Nevark AI Backend Started"
    )

# ============================================================
# SHUTDOWN EVENT
# ============================================================

@app.on_event("shutdown")
async def shutdown_event():

    logger.info(
        "🛑 Nevark AI Backend Stopped"
    )