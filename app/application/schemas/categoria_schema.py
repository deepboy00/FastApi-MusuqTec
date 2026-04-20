from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CategoriaCreate(BaseModel):
    nombre: str
    slug: str
    icono: Optional[str] = None
    activo: bool = True


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    slug: Optional[str] = None
    icono: Optional[str] = None
    activo: Optional[bool] = None


class CategoriaOut(BaseModel):
    id: int
    nombre: str
    slug: str
    icono: Optional[str] = None
    activo: bool
    created_at: datetime

    model_config = {"from_attributes": True}
