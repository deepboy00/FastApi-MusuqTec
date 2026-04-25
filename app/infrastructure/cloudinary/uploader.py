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


def extract_public_id(url: str) -> str | None:
    """
    Extrae el public_id de una URL de Cloudinary.

    Maneja URLs con y sin transformaciones:
      .../upload/v1234/musuq_tec/productos/prod_abc.webp
      .../upload/w_1200,c_limit,q_auto,f_auto/v1234/musuq_tec/productos/prod_abc.webp

    Devuelve: musuq_tec/productos/prod_abc
    Devuelve None si la URL no es de Cloudinary.
    """
    if not url or "cloudinary.com" not in url:
        return None
    try:
        after_upload = url.split("/upload/", 1)[1]

        # Consumir segmentos que sean transformaciones (contienen "=" o "_")
        # o versiones (empiezan con "v" seguido de dígitos).
        # El public_id empieza cuando encontramos un segmento que es parte de la ruta real.
        segments = after_upload.split("/")
        path_segments = []
        for seg in segments:
            # Segmento de transformación: contiene "_" como separador de parámetro (ej: w_1200, c_limit)
            # Segmento de versión: empieza con "v" y el resto son dígitos (ej: v1734512345)
            is_transform = "_" in seg and not seg.startswith("prod_") and not seg.startswith("musuq")
            is_version = seg.startswith("v") and seg[1:].isdigit()
            if is_transform or is_version:
                continue
            path_segments.append(seg)

        public_id = "/".join(path_segments)

        # Quitar extensión del último segmento
        if "." in public_id.split("/")[-1]:
            public_id = public_id.rsplit(".", 1)[0]

        return public_id if public_id else None
    except Exception:
        return None
