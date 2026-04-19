from dataclasses import dataclass
from typing import Optional


@dataclass
class Banner:
    titulo: str
    subtitulo: str
    imagen_url: str
    orden: int = 0
    id: Optional[int] = None
    activo: bool = True
    link: Optional[str] = None
