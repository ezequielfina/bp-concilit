from __future__ import annotations
from typing import List, TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.conciliaciones.alicuotas.CargaAlicuota import CargaAlicuota
from utils.engine_db import Base

if TYPE_CHECKING:
    from models.conciliaciones.Cuenta import Cuenta

class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    razon_social: Mapped[str] = mapped_column(index=True)
    cuit: Mapped[str] = mapped_column(unique=True)

    cuentas: Mapped[List["Cuenta"]] = relationship(back_populates="empresa")

    cargas_alicuota: Mapped[List["CargaAlicuota"]] = relationship(back_populates='empresa')
