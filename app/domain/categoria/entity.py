from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Categoria:
    nombre: str
    slug: str
    id: Optional[int] = None
    icono: Optional[str] = None
    activo: bool = True
    created_at: Optional[datetime] = None
