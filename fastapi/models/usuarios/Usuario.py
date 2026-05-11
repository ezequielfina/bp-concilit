import datetime

from sqlalchemy.orm import mapped_column, Mapped
from utils.engine_db import Base
from uuid import UUID
from datetime import timezone

class Usuario(Base):
    __tablename__ = 'usuarios'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[timezone] = mapped_column(default=datetime.datetime)
    updated_at: Mapped[timezone]
    rol: Mapped[str]
