import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.deps import get_current_admin
from app.application.schemas.producto_schema import ProductoCreate, ProductoOut, ProductoUpdate
from app.core.database import get_db
from app.domain.producto.entity import Producto, ProductoSpec
from app.infrastructure.cloudinary.uploader import upload_product_image
from app.infrastructure.db.repositories.producto_repo import ProductoRepository
from app.infrastructure.db.repositories.producto_spec_repo import ProductoSpecRepository

router = APIRouter(prefix="/productos", tags=["productos"])

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


def _producto_out(p: Producto) -> ProductoOut:
    return ProductoOut(
        id=p.id,
        nombre=p.nombre,
        slug=p.slug,
        sku=p.sku,
        tagline=p.tagline,
        descripcion=p.descripcion,
        precio=p.precio,
        stock=p.stock,
        categoria_id=p.categoria_id,
        imagen_url=p.imagen_url,
        imagen_thumb=p.imagen_thumb,
        activo=p.activo,
        vistas=p.vistas,
        wsp_clicks=p.wsp_clicks,
        specs=[{"id": s.id, "spec": s.spec, "orden": s.orden} for s in p.specs],
        created_at=p.created_at,
        updated_at=p.updated_at,
    )


# ── Endpoints públicos ────────────────────────────────────────

@router.get("/", response_model=list[ProductoOut])
async def listar_productos(
    db: Annotated[AsyncSession, Depends(get_db)],
    categoria_id: int | None = None,
) -> list[ProductoOut]:
    repo = ProductoRepository(db)
    if categoria_id:
        productos = await repo.get_by_categoria(categoria_id)
    else:
        productos = await repo.get_all(activo_only=True)
    return [_producto_out(p) for p in productos]


@router.get("/{producto_id}", response_model=ProductoOut)
async def obtener_producto(
    producto_id: int, db: Annotated[AsyncSession, Depends(get_db)]
) -> ProductoOut:
    repo = ProductoRepository(db)
    p = await repo.get_by_id(producto_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return _producto_out(p)


# ── Endpoints protegidos (admin) ──────────────────────────────

@router.post("/", response_model=ProductoOut, status_code=status.HTTP_201_CREATED)
async def crear_producto(
    nombre: Annotated[str, Form()],
    slug: Annotated[str, Form()],
    sku: Annotated[str, Form()],
    precio: Annotated[float, Form()],
    stock: Annotated[int, Form()],
    imagen: Annotated[UploadFile, File()],
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[dict, Depends(get_current_admin)],
    categoria_id: Annotated[int | None, Form()] = None,
    tagline: Annotated[str | None, Form()] = None,
    descripcion: Annotated[str | None, Form()] = None,
    activo: Annotated[bool, Form()] = True,
) -> ProductoOut:
    file_bytes = await _validate_image(imagen)
    public_id = f"prod_{uuid.uuid4().hex}"
    imagen_url, imagen_thumb = upload_product_image(file_bytes, public_id)

    repo = ProductoRepository(db)
    p = await repo.create(
        Producto(
            nombre=nombre,
            slug=slug,
            sku=sku,
            tagline=tagline,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria_id=categoria_id,
            activo=activo,
            imagen_url=imagen_url,
            imagen_thumb=imagen_thumb,
        )
    )
    return _producto_out(p)


@router.put("/{producto_id}", response_model=ProductoOut)
async def actualizar_producto(
    producto_id: int,
    body: ProductoUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[dict, Depends(get_current_admin)],
) -> ProductoOut:
    repo = ProductoRepository(db)
    spec_repo = ProductoSpecRepository(db)
    p = await repo.get_by_id(producto_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    for field, value in body.model_dump(exclude_none=True, exclude={"specs"}).items():
        setattr(p, field, value)
    updated = await repo.update(p)

    if body.specs is not None:
        nuevas = await spec_repo.replace_all(
            producto_id, [ProductoSpec(spec=s.spec, orden=s.orden) for s in body.specs]
        )
        updated.specs = nuevas

    return _producto_out(updated)


@router.patch("/{producto_id}/imagen", response_model=ProductoOut)
async def actualizar_imagen(
    producto_id: int,
    imagen: Annotated[UploadFile, File()],
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[dict, Depends(get_current_admin)],
) -> ProductoOut:
    repo = ProductoRepository(db)
    p = await repo.get_by_id(producto_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    file_bytes = await _validate_image(imagen)
    public_id = f"prod_{uuid.uuid4().hex}"
    imagen_url, imagen_thumb = upload_product_image(file_bytes, public_id)
    p.imagen_url = imagen_url
    p.imagen_thumb = imagen_thumb
    updated = await repo.update(p)
    return _producto_out(updated)


@router.patch("/{producto_id}/stock", response_model=ProductoOut)
async def decrementar_stock(
    producto_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[dict, Depends(get_current_admin)],
    cantidad: int = 1,
) -> ProductoOut:
    repo = ProductoRepository(db)
    try:
        p = await repo.decrement_stock(producto_id, cantidad)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return _producto_out(p)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(
    producto_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[dict, Depends(get_current_admin)],
) -> None:
    repo = ProductoRepository(db)
    p = await repo.get_by_id(producto_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    await repo.delete(producto_id)
