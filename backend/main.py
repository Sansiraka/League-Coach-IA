from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import sync, analytics, coaching

app = FastAPI(
    title="League Coach IA API",
    description="Backend para el coach personal de League of Legends",
    version="1.0.0"
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
