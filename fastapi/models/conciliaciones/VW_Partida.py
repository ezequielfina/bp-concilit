from typing import Optional
from uuid import UUID
from sqlalchemy.dialects.postgresql import DATE, NUMERIC
from utils.engine_db import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date


class VWPartida(Base):
    __tablename__ = 'vw_partidas_visualizacion'

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    asignacion: Mapped[str] = mapped_column(nullable=False, index=True)
    fecha_doc: Mapped[date] = mapped_column(index=True, nullable=False)
    importe_valorado_ml2: Mapped[NUMERIC] = mapped_column(NUMERIC(18, 2))
    anterior: Mapped[bool]
    id_cuenta: Mapped[UUID]
    id_carga_mayor: Mapped[Optional[UUID]]
    estado: Mapped[str]
    activo: Mapped[bool]
    comentario: Mapped[Optional[UUID]]

    __table_args__ = {"extend_existing": True}
