from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.deps import get_current_admin
from app.application.schemas.categoria_schema import CategoriaCreate, CategoriaOut, CategoriaUpdate
from app.core.database import get_db
from app.domain.categoria.entity import Categoria
from app.infrastructure.db.repositories.categoria_repo import CategoriaRepository

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("/", response_model=list[CategoriaOut])
async def listar_categorias(db: Annotated[AsyncSession, Depends(get_db)]) -> list[CategoriaOut]:
    repo = CategoriaRepository(db)
    cats = await repo.get_all()
    return [CategoriaOut(**cat.__dict__) for cat in cats]


@router.get("/{categoria_id}", response_model=CategoriaOut)
async def obtener_categoria(
    categoria_id: int, db: Annotated[AsyncSession, Depends(get_db)]
) -> CategoriaOut:
    repo = CategoriaRepository(db)
    cat = await repo.get_by_id(categoria_id)
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return CategoriaOut(**cat.__dict__)


@router.post("/", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
async def crear_categoria(
    body: CategoriaCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[dict, Depends(get_current_admin)],
) -> CategoriaOut:
    repo = CategoriaRepository(db)
    existing = await repo.get_by_slug(body.slug)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El slug ya existe")
    cat = await repo.create(Categoria(nombre=body.nombre, slug=body.slug, icono=body.icono, activo=body.activo))
    return CategoriaOut(**cat.__dict__)


@router.put("/{categoria_id}", response_model=CategoriaOut)
async def actualizar_categoria(
    categoria_id: int,
    body: CategoriaUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[dict, Depends(get_current_admin)],
) -> CategoriaOut:
    repo = CategoriaRepository(db)
    cat = await repo.get_by_id(categoria_id)
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    if body.nombre is not None:
        cat.nombre = body.nombre
    if body.slug is not None:
        cat.slug = body.slug
    if body.icono is not None:
        cat.icono = body.icono
    if body.activo is not None:
        cat.activo = body.activo
    updated = await repo.update(cat)
    return CategoriaOut(**updated.__dict__)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_categoria(
    categoria_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[dict, Depends(get_current_admin)],
) -> None:
    repo = CategoriaRepository(db)
    cat = await repo.get_by_id(categoria_id)
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    await repo.delete(categoria_id)
