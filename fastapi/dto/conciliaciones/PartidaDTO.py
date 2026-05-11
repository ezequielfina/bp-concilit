from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from typing import Optional
from decimal import Decimal


class PartidaSchema(BaseModel):
    id: UUID
    # Campos que suelen ser obligatorios en el negocio
    asignacion: str = Field(max_length=64)
    fecha_doc: date
    importe_valorado_ml2: Decimal = Field(max_digits=12, decimal_places=2)
    anterior: bool
    id_cuenta: UUID
    id_carga_mayor: Optional[UUID]
    estado: Optional[str]
    activo: Optional[bool]
    comentario: Optional[str]
