from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID


class CuentaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=64)
    comentario: Optional[str] = Field(..., min_length=1, max_length=256)

    id_empresa: UUID


class CuentaCreate(CuentaBase):
    pass


class CuentaSchema(CuentaBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class CuentaUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=64)
    comentario: Optional[str] = Field(default=None, min_length=1, max_length=256)
