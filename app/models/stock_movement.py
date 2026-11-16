from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.user import User


class StockMovement(Base):
    __tablename__ = "movimientos_stock"
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="check_cantidad_positiva"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    id_producto: Mapped[int] = mapped_column(Integer, ForeignKey("productos.id"), nullable=False, index=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    tipo_movimiento: Mapped[str] = mapped_column(String(50), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_movimiento: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    producto: Mapped["Product"] = relationship("Product", back_populates="movimientos")
    usuario: Mapped["User"] = relationship("User", back_populates="movimientos")

    def __repr__(self) -> str:
        return f"<StockMovement(id={self.id}, tipo='{self.tipo_movimiento}', cantidad={self.cantidad})>"
