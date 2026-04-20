from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Admin:
    username: str
    password_hash: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
