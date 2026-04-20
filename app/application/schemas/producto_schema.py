from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class ProductoSpecOut(BaseModel):
    id: int
    spec: str
    orden: int

    model_config = {"from_attributes": True}


class ProductoSpecIn(BaseModel):
    spec: str
    orden: int = 0


class ProductoCreate(BaseModel):
    nombre: str
    slug: str
    sku: str
    precio: float
    stock: int
    categoria_id: Optional[int] = None
    tagline: Optional[str] = None
    descripcion: Optional[str] = None
    activo: bool = True
    specs: list[ProductoSpecIn] = []

    @field_validator("precio")
    @classmethod
    def precio_positivo(cls, v: float) -> float:
        if v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v

    @field_validator("stock")
    @classmethod
    def stock_no_negativo(cls, v: int) -> int:
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    slug: Optional[str] = None
    sku: Optional[str] = None
    tagline: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    categoria_id: Optional[int] = None
    activo: Optional[bool] = None
    specs: Optional[list[ProductoSpecIn]] = None


class ProductoOut(BaseModel):
    id: int
    nombre: str
    slug: str
    sku: str
    tagline: Optional[str] = None
    descripcion: Optional[str] = None
    precio: float
    stock: int
    categoria_id: Optional[int] = None
    imagen_url: Optional[str] = None
    imagen_thumb: Optional[str] = None
    activo: bool
    vistas: int
    wsp_clicks: int
    specs: list[ProductoSpecOut] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
