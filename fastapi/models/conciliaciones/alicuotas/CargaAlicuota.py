import datetime
import uuid
from typing import List

from utils.engine_db import Base
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class CargaAlicuota(Base):
    __tablename__ = 'ali_cargas'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    fecha_carga: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now, nullable=False)
    comentario: Mapped[str] = mapped_column(String(150), nullable=True)
    estado: Mapped[str] = mapped_column(String(100), nullable=False)
    activo: Mapped[bool] = mapped_column(default=True)

    id_empresa: Mapped[UUID] = mapped_column(ForeignKey('empresas.id', ondelete='CASCADE'), nullable=False)

    id_jurisdiccion: Mapped[UUID] = mapped_column(ForeignKey('ali_jurisdicciones.id', ondelete='CASCADE'), nullable=False)

    empresa: Mapped["Empresa"] = relationship(back_populates='cargas_alicuota')

    jurisdiccion: Mapped["Jurisdiccion"] = relationship(back_populates='cargas_alicuota')
