import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.deps import get_current_admin
from app.application.schemas.banner_schema import BannerOut, BannerUpdate
from app.core.database import get_db
from app.domain.banner.entity import Banner
from app.infrastructure.cloudinary.uploader import upload_product_image
from app.infrastructure.db.repositories.banner_repo import BannerRepository

router = APIRouter(prefix="/banners", tags=["banners"])

_ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
_MAX_SIZE = 5 * 1024 * 1024


async def _validate_image(file: UploadFile) -> bytes:
    if file.content_type not in _ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Formato no permitido. Usa JPG, PNG o WEBP.",
        )
    data = await file.read()
    if len(data) > _MAX_SIZE:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La imagen supera el límite de 5 MB.",
        )
    return data


@router.get("/", response_model=list[BannerOut])
async def listar_banners(db: Annotated[AsyncSession, Depends(get_db)]) -> list[BannerOut]:
    repo = BannerRepository(db)
    banners = await repo.get_all(activo_only=True)
    return [BannerOut(**b.__dict__) for b in banners]


@router.post("/", response_model=BannerOut, status_code=status.HTTP_201_CREATED)
async def crear_banner(
    titulo: Annotated[str, Form()],
    imagen: Annotated[UploadFile, File()],
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[dict, Depends(get_current_admin)],
    subtitulo: Annotated[str, Form()] = "",
    orden: Annotated[int, Form()] = 0,
    activo: Annotated[bool, Form()] = True,
    link: Annotated[str | None, Form()] = None,
) -> BannerOut:
    file_bytes = await _validate_image(imagen)
    public_id = f"banner_{uuid.uuid4().hex}"
    imagen_url, _ = upload_product_image(file_bytes, public_id)

    repo = BannerRepository(db)
    b = await repo.create(
        Banner(titulo=titulo, subtitulo=subtitulo, imagen_url=imagen_url, orden=orden, activo=activo, link=link)
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
