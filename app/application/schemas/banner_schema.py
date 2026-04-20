from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BannerCreate(BaseModel):
    titulo: str
    subtitulo: Optional[str] = None
    orden: int = 0
    activo: bool = True


class BannerUpdate(BaseModel):
    titulo: Optional[str] = None
    subtitulo: Optional[str] = None
    orden: Optional[int] = None
    activo: Optional[bool] = None


class BannerOut(BaseModel):
    id: int
    titulo: str
    subtitulo: Optional[str] = None
    activo: bool
    orden: int
    created_at: datetime

    model_config = {"from_attributes": True}
