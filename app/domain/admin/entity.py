from dataclasses import dataclass
from typing import Optional


@dataclass
class Admin:
    email: str
    hashed_password: str
    id: Optional[int] = None
    nombre: str = ""
    activo: bool = True
