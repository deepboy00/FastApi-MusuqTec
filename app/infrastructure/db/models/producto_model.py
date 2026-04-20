from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ProductoModel(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    tagline: Mapped[str | None] = mapped_column(String(300), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    precio: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sku: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    categoria_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("categorias.id"), nullable=True
    )
    imagen_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    imagen_thumb: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    vistas: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    wsp_clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    categoria: Mapped["CategoriaModel"] = relationship(
        "CategoriaModel", back_populates="productos", lazy="joined"
    )
    specs: Mapped[list["ProductoSpecModel"]] = relationship(
        "ProductoSpecModel", back_populates="producto", cascade="all, delete-orphan", lazy="select"
    )
