from uuid import UUID
from pydantic import BaseModel, Field


class JurisdiccionBase(BaseModel):
    nombre: str = Field(..., max_length=60)


class JurisdiccionCreate(JurisdiccionBase):
    pass


class JurisdiccionSchema(JurisdiccionBase):
    id: UUID
