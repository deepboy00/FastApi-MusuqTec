import cloudinary
import cloudinary.uploader

from app.core.config import settings

# Configurar Cloudinary una sola vez al importar el módulo
cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True,
)


def upload_product_image(file_bytes: bytes, public_id: str) -> tuple[str, str]:
    """
    Sube una imagen a Cloudinary y devuelve (imagen_url, imagen_thumb).
    - imagen_url  : URL original (c_limit, w_1200)
    - imagen_thumb: URL recortada a 400x400 (c_fill, g_center)
    """
    result = cloudinary.uploader.upload(
        file_bytes,
        public_id=public_id,
        folder="musuq_tec/productos",
        overwrite=True,
        resource_type="image",
        transformation=[{"width": 1200, "crop": "limit", "quality": "auto", "fetch_format": "auto"}],
    )

    imagen_url: str = result["secure_url"]

    imagen_thumb: str = cloudinary.CloudinaryImage(result["public_id"]).build_url(
        width=400,
        height=400,
        crop="fill",
        gravity="center",
        quality="auto",
        fetch_format="auto",
        secure=True,
    )

    return imagen_url, imagen_thumb


def delete_image(public_id: str) -> None:
    """Elimina una imagen de Cloudinary dado su public_id."""
    cloudinary.uploader.destroy(public_id, resource_type="image")
