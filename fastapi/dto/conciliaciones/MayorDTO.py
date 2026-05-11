from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import date
from decimal import Decimal


class MayorBase(BaseModel):
    # Campos que suelen ser obligatorios en el negocio
    asignacion: str = Field(max_length=64)
    ejercicio_mes: date
    fecha_doc: date
    fecha_contabilizacion: date
    importe_valorado_ml2: Decimal = Field(max_digits=12, decimal_places=2)
    anterior: bool
    id_cuenta: UUID

    # Campos que fallaron porque en la DB son NULL (None)
    # Deben ser Optional y tener default=None
    sociedad: Optional[str] = Field(default=None, max_length=32)
    cuenta: Optional[str] = Field(default=None, max_length=32)
    documento: Optional[str] = Field(default=None, max_length=32)
    clase_doc: Optional[str] = Field(default=None, max_length=32)
    clave_contabilizacion: Optional[str] = Field(default=None, max_length=32)

    importe_moneda_doc: Optional[Decimal] = Field(default=None, max_digits=12, decimal_places=2)
    moneda_doc: Optional[str] = Field(default=None, max_length=16)
    importe_moneda_local: Optional[Decimal] = Field(default=None, max_digits=12, decimal_places=2)
    moneda_local: Optional[str] = Field(default=None, max_length=16)

    # Estos son los que te marcaron el error específicamente
    texto_cab_doc: Optional[str] = Field(default=None, max_length=512)
    texto: Optional[str] = Field(default=None, max_length=512)
    cuenta_contrapartida: Optional[str] = Field(default=None, max_length=32)
    referencia: Optional[str] = Field(default=None, max_length=512)


class MayorCreate(MayorBase):
    pass


class MayorSchema(MayorBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class MayorUpdate(BaseModel):
    sociedad: Optional[str] = Field(default= None, max_length=32)
    cuenta: Optional[str] = Field(default= None, max_length=32)
    asignacion: Optional[str] = Field(default= None, max_length=64)
    documento: Optional[str] = Field(default= None, max_length=32)
    ejercicio_mes: Optional[date] = Field(default=None)
    clase_doc: Optional[str] = Field(default= None, max_length=32)
    fecha_doc: Optional[date] = Field(default=None)
    fecha_contabilizacion: Optional[date] = Field(default=None)
    clave_contabilizacion: Optional[str] = Field(default= None, max_length=32)
    importe_moneda_doc: Optional[Decimal] = Field(default=None, max_digits=12, decimal_places=2)
    moneda_doc: Optional[str] = Field(default= None, max_length=16)
    importe_moneda_local: Optional[Decimal] = Field(default=None, max_digits=12, decimal_places=2)
    moneda_local: Optional[str] = Field(default= None, max_length=16)
    texto_cab_doc: Optional[str] = Field(default= None, max_length=512)
    texto: Optional[str] = Field(default= None, max_length=512)
    cuenta_contrapartida: Optional[str] = Field(default= None, max_length=32)
    referencia: Optional[str] = Field(default= None, max_length=512)
    importe_valorado_ml2: Optional[Decimal] = Field(default= None, max_digits=12, decimal_places=2)
    anterior: Optional[bool] = Field(default= None)
