from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


class EmpresaBase(BaseModel):
    razon_social: str = Field(..., min_length= 1,max_length=64)
    cuit: str = Field(
        ...,
        pattern=r"^\d{11}$",
        examples=["20304005001"], min_length=11, max_length=11)


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaSchema(EmpresaBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class EmpresaUpdate(BaseModel):
    razon_social: Optional[str] = Field(default=None, min_length=1, max_length=64)
    cuit: Optional[str] = Field(default=None,
        pattern=r"^\d{11}$",
        examples=["20304005001"], min_length=11, max_length=11)
