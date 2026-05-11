from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import date
from decimal import Decimal


class SaldoBancarioBase(BaseModel):
    fecha: date
    saldo_ars: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    saldo_usd: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    id_cuenta: UUID


class SaldoBancarioCreate(SaldoBancarioBase):
    pass


class SaldoBancarioSchema(SaldoBancarioBase):
    id: UUID
    status_reporte: str = Field(max_length=60)
    extension_reporte: Optional[str] = Field(default=None, max_length=60)

    model_config = ConfigDict(from_attributes=True)


class SaldoBancarioUpdate(BaseModel):
    fecha: Optional[date] = Field(default=None)
    saldo_ars: Optional[Decimal] = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    saldo_usd: Optional[Decimal] = Field(default=None, ge=0, max_digits=12, decimal_places=2)
