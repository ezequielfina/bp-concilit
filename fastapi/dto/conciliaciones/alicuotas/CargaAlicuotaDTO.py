from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class CargaAlicuotaBase(BaseModel):
    id_empresa: UUID
    id_jurisdiccion: UUID
    comentario: Optional[str] = Field(default=None, max_length=150)


class CargaAlicuotaCreate(CargaAlicuotaBase):
    pass


class CargaAlicuotaSchema(CargaAlicuotaBase):
    id: UUID
    fecha_carga: datetime = Field(default=datetime.now)
    estado: str = Field(max_length=100)
    activo: bool = Field(default=True)

