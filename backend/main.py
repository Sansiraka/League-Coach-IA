from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback
from api.routes import sync, analytics, coaching
from db.database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear las tablas en la base de datos si no existen
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="League Coach IA API",
    description="Backend para el coach personal de League of Legends",
    version="1.0.0",
    lifespan=lifespan
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "traceback": traceback.format_exc()}
    )

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción restringir a localhost:5173 o dominio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sync.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(coaching.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend is running!"}
