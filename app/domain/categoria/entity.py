from dataclasses import dataclass
from typing import Optional


@dataclass
class Categoria:
    nombre: str
    slug: str
    id: Optional[int] = None
    activo: bool = True
