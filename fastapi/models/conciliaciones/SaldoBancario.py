from __future__ import annotations
import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, DATE, NUMERIC
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from utils.engine_db import Base

if TYPE_CHECKING:
    from models.conciliaciones.Cuenta import Cuenta


class SaldoBancario(Base):
    __tablename__ = "saldos_bancarios"

    # Definición de columnas con Mapped
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid4
    )

    fecha: Mapped[datetime.date] = mapped_column(
        DATE,
        nullable=False,
        default=datetime.date.today
    )

    saldo_ars: Mapped[float] = mapped_column(
        NUMERIC(12, 2),
        nullable=False
    )

    saldo_usd: Mapped[float] = mapped_column(
        NUMERIC(12, 2),
        nullable=False
    )

    # Asumiendo que status_reporte es un string, ajústalo si es Enum o int
    status_reporte: Mapped[str] = mapped_column(default='No solicitado', nullable=False)

    # Asumiendo que status_reporte es un string, ajústalo si es Enum o int
    extension_reporte: Mapped[str | None] = mapped_column(default=None, nullable=True)

    # Clave foránea
    id_cuenta: Mapped[UUID] = mapped_column(
        ForeignKey("cuentas.id"),
        nullable=False
    )

    # Relación
    cuenta: Mapped["Cuenta"] = relationship(
        back_populates="saldos_bancarios"
    )