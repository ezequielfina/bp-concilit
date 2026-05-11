from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.engine_db import Base
from uuid import UUID, uuid4
from sqlalchemy import String


class Jurisdiccion(Base):
    __tablename__ = 'ali_jurisdicciones'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)

    cargas_alicuota: Mapped[List["CargaAlicuota"]] = relationship(back_populates='jurisdiccion')


