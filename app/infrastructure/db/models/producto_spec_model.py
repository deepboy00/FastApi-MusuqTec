from sqlalchemy import ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ProductoSpecModel(Base):
    __tablename__ = "producto_specs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    producto_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("productos.id", ondelete="CASCADE"), nullable=False
    )
    spec: Mapped[str] = mapped_column(String(300), nullable=False)
    orden: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)

    producto: Mapped["ProductoModel"] = relationship(
        "ProductoModel", back_populates="specs"
    )
