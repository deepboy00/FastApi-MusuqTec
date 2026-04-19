from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Producto:
    nombre: str
    descripcion: str
    precio: float
    stock: int
    categoria_id: int
    imagen_url: str
    imagen_thumb: str
    id: Optional[int] = None
    activo: bool = True
    destacado: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
