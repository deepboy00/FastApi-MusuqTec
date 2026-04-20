from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.deps import get_current_admin
from app.application.schemas.banner_schema import BannerCreate, BannerOut, BannerUpdate
from app.core.database import get_db
from app.domain.banner.entity import Banner
from app.infrastructure.db.repositories.banner_repo import BannerRepository

router = APIRouter(prefix="/banners", tags=["banners"])


@router.get("/", response_model=list[BannerOut])
async def listar_banners(db: Annotated[AsyncSession, Depends(get_db)]) -> list[BannerOut]:
    repo = BannerRepository(db)
    banners = await repo.get_all(activo_only=True)
    return [BannerOut(**b.__dict__) for b in banners]


@router.post("/", response_model=BannerOut, status_code=status.HTTP_201_CREATED)
async def crear_banner(
    body: BannerCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[dict, Depends(get_current_admin)],
) -> BannerOut:
    repo = BannerRepository(db)
    b = await repo.create(
        Banner(titulo=body.titulo, subtitulo=body.subtitulo, orden=body.orden, activo=body.activo)
    )
    return BannerOut(**b.__dict__)


@router.put("/{banner_id}", response_model=BannerOut)
async def actualizar_banner(
    banner_id: int,
    body: BannerUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[dict, Depends(get_current_admin)],
) -> BannerOut:
    repo = BannerRepository(db)
    b = await repo.get_by_id(banner_id)
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banner no encontrado")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(b, field, value)
    updated = await repo.update(b)
    return BannerOut(**updated.__dict__)


@router.delete("/{banner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_banner(
    banner_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[dict, Depends(get_current_admin)],
) -> None:
    repo = BannerRepository(db)
    b = await repo.get_by_id(banner_id)
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Banner no encontrado")
    await repo.delete(banner_id)
