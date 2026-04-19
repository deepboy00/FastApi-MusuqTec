from pydantic import BaseModel


class CategoriaCreate(BaseModel):
    nombre: str
    slug: str
    activo: bool = True


class CategoriaUpdate(BaseModel):
    nombre: str | None = None
    slug: str | None = None
    activo: bool | None = None


class CategoriaOut(BaseModel):
    id: int
    nombre: str
    slug: str
    activo: bool

    model_config = {"from_attributes": True}
