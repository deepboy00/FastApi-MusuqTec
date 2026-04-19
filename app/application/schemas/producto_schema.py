from datetime import datetime
from pydantic import BaseModel, field_validator


class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str = ""
    precio: float
    stock: int
    categoria_id: int
    activo: bool = True
    destacado: bool = False

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
    nombre: str | None = None
    descripcion: str | None = None
    precio: float | None = None
    stock: int | None = None
    categoria_id: int | None = None
    activo: bool | None = None
    destacado: bool | None = None


class ProductoOut(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    stock: int
    activo: bool
    destacado: bool
    imagen_url: str
    imagen_thumb: str
    categoria_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
