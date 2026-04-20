"""
Script para crear el primer admin en la base de datos.
Uso:
    python seed_admin.py
"""
import asyncio
import os

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# ── Configuración ─────────────────────────────────────────────
# Cambia estos valores antes de ejecutar
USERNAME = "aquino"
PASSWORD = "Angelo@1234"

# Lee DATABASE_URL del entorno o del .env
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("No se encontró DATABASE_URL en el entorno o .env")

# Asegurarse que use asyncpg
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)


# ── Lógica ────────────────────────────────────────────────────
async def create_admin():
    engine = create_async_engine(DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    hashed = bcrypt.hashpw(PASSWORD.encode(), bcrypt.gensalt()).decode()

    async with SessionLocal() as session:
        # Crear tabla si no existe (por si acaso)
        from app.core.database import Base
        from app.infrastructure.db.models.admin_model import AdminModel  # noqa: F401

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Verificar si ya existe
        from sqlalchemy import select
        result = await session.execute(
            select(AdminModel).where(AdminModel.username == USERNAME)
        )
        existing = result.scalar_one_or_none()

        if existing:
            print(f"⚠️  Ya existe un admin con el username '{USERNAME}'")
        else:
            admin = AdminModel(
                username=USERNAME,
                password_hash=hashed,
            )
            session.add(admin)
            await session.commit()
            print(f"✅ Admin creado exitosamente")
            print(f"   Username: {USERNAME}")
            print(f"   Password: {PASSWORD}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_admin())
