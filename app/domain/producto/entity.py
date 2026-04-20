from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ProductoSpec:
    spec: str
    orden: int = 0
    id: Optional[int] = None


@dataclass
class Producto:
    nombre: str
    slug: str
    precio: float
    stock: int
    sku: str
    id: Optional[int] = None
    tagline: Optional[str] = None
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    imagen_url: Optional[str] = None
    imagen_thumb: Optional[str] = None
    activo: bool = True
    vistas: int = 0
    wsp_clicks: int = 0
    specs: list[ProductoSpec] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
