from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.stock_movement import StockMovement


class User(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(50), nullable=False, default="Cliente")
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relación 1 a N: Un usuario registra muchos movimientos de stock
    movimientos: Mapped[List["StockMovement"]] = relationship("StockMovement", back_populates="usuario")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', rol='{self.rol}')>"
