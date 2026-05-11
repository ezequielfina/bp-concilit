from __future__ import annotations  # 1. Evita errores de referencia circular
import uuid
from uuid import UUID
from typing import TYPE_CHECKING  # Para evitar importaciones circulares en runtime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from utils.engine_db import Base

# 2. Solo importamos Empresa para el autocompletado del editor,
# pero no se ejecuta en tiempo de ejecución de Python.
if TYPE_CHECKING:
    from models.Empresa import Empresa
    from models.conciliaciones.SaldoBancario import SaldoBancario
    from models.conciliaciones.Mayor import Mayor
    from models.conciliaciones.CargaMayor import CargaMayor


class Cuenta(Base):
    __tablename__ = "cuentas"

    # En SQLAlchemy 2.0, usamos Mapped[tipo]
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(64), nullable=False)
    comentario: Mapped[str] = mapped_column(String(256), nullable=False)

    # id_empresa debe coincidir con el tipo de la PK de Empresa (UUID)
    id_empresa: Mapped[UUID] = mapped_column(ForeignKey("empresas.id", ondelete="CASCADE"))

    # Usamos el nombre de la clase como string "Empresa"
    empresa: Mapped["Empresa"] = relationship(back_populates="cuentas")

    saldos_bancarios: Mapped[list["SaldoBancario"]] = relationship(back_populates="cuenta")

    partidas: Mapped[list["Mayor"]] = relationship(back_populates="rel_cuenta")

    cargas_mayor: Mapped[list["CargaMayor"]] = relationship(back_populates="cuentas")

    def __repr__(self) -> str:
        return f"<Cuenta(id={self.id}, nombre='{self.nombre}')>"
