from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.routers import auth_router, banner_router, categoria_router, producto_router
from app.core.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Crea las tablas si no existen (en prod usa Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="MUSUQ TEC API",
    description="Backend para la tienda de equipos POS MUSUQ TEC",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restringe a tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────
app.include_router(auth_router.router)
app.include_router(categoria_router.router)
app.include_router(producto_router.router)
app.include_router(banner_router.router)


@app.get("/", tags=["health"])
async def root() -> dict:
    return {"status": "ok", "app": "MUSUQ TEC API"}
