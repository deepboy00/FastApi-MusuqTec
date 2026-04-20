from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Banner:
    titulo: str
    id: Optional[int] = None
    subtitulo: Optional[str] = None
    activo: bool = True
    orden: int = 0
    created_at: Optional[datetime] = None
