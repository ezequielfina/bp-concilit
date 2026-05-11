from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class CargaMayorBase(BaseModel):
    fecha_carga: datetime = Field(default=datetime.now)
    id_cuenta: UUID
    activo: bool = Field(default=True)
    comentario: str | None = Field(default=None, max_length=120)
    estado: str = Field(default='Pendiente', max_length=30)


class CargaMayorSchema(CargaMayorBase):
    id: UUID


class CargaMayorCreate(CargaMayorBase):
    pass
