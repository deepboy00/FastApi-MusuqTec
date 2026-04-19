from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BannerModel(Base):
    __tablename__ = "banners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    subtitulo: Mapped[str] = mapped_column(Text, nullable=False, default="")
    imagen_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    orden: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
