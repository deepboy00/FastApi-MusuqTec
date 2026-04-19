from pydantic import BaseModel


class BannerCreate(BaseModel):
    titulo: str
    subtitulo: str = ""
    orden: int = 0
    activo: bool = True
    link: str | None = None


class BannerUpdate(BaseModel):
    titulo: str | None = None
    subtitulo: str | None = None
    orden: int | None = None
    activo: bool | None = None
    link: str | None = None


class BannerOut(BaseModel):
    id: int
    titulo: str
    subtitulo: str
    imagen_url: str
    orden: int
    activo: bool
    link: str | None

    model_config = {"from_attributes": True}
