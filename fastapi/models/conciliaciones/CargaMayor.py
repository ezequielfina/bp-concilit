from typing import TYPE_CHECKING, Optional, List
from utils.engine_db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, CheckConstraint, text, func
import uuid
from uuid import UUID
from datetime import datetime

if TYPE_CHECKING:
    from models.conciliaciones.Cuenta import Cuenta
    from models.conciliaciones.Mayor import Mayor


class CargaMayor(Base):
    __tablename__ = 'cargas_mayor'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    fecha_carga: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )

    activo: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )

    # Coincide con tu DEFAULT 'Pendiente' y el NOT NULL
    estado: Mapped[str] = mapped_column(
        String(30),
        server_default=text("'Pendiente'"),
        nullable=False
    )

    comentario: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)

    id_cuenta: Mapped[UUID] = mapped_column(
        ForeignKey("cuentas.id", ondelete='CASCADE'),
        nullable=False
    )

    cuentas: Mapped["Cuenta"] = relationship("Cuenta", back_populates="cargas_mayor")

    partidas: Mapped[List["Mayor"]] = relationship(back_populates="carga_mayor")

    # Constraint de estados (opcional en el modelo, pero bueno para coherencia)
    __table_args__ = (
        CheckConstraint(
            estado.in_([
                'Pendiente', 'Validando', 'Transformando',
                'Cargando data en DB', 'Cargado OK', 'Falló', 'Archivo no válido'
            ]),
            name='ck_carga_mayor'
        ),
    )