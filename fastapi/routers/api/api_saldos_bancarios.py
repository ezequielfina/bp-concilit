from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from utils.engine_db import get_db # Tu generador de sesión
from dto.conciliaciones.SaldoBancarioDTO import SaldoBancarioCreate, SaldoBancarioSchema, SaldoBancarioUpdate
from services.conciliaciones.service_saldos_bancarios import (
    nuevo_saldo_bancario,
    get_saldos_bancarios_by_id_cuenta_json,
    get_saldo_bancario_by_id_json,
    update_saldo
)


api_saldos_bancarios = APIRouter(prefix="/saldos_bancarios", tags=["Saldos"])


@api_saldos_bancarios.post("", response_model=SaldoBancarioSchema)
def crear_saldo_bancario(saldo_bancario: SaldoBancarioCreate, db: Session = Depends(get_db)):
    return nuevo_saldo_bancario(saldo_data=saldo_bancario, db=db)


@api_saldos_bancarios.get("/cuenta/{id_cuenta}", response_model=list[SaldoBancarioSchema])
def obtener_saldos_bancarios_by_id_cuenta(id_cuenta: UUID, db: Session = Depends(get_db)):
    return get_saldos_bancarios_by_id_cuenta_json(id_cuenta=id_cuenta, db=db)


@api_saldos_bancarios.get("/{id}", response_model=SaldoBancarioSchema)
def obtener_saldo_bancario_by_id(id: UUID, db: Session = Depends(get_db)):
    return get_saldo_bancario_by_id_json(id=id, db=db)


@api_saldos_bancarios.put("/{id}", response_model=SaldoBancarioSchema)
def modificar_saldo_bancario(
        id: UUID,
        payload: SaldoBancarioUpdate,
        db: Session = Depends(get_db)
):
    # Delegamos toda la lógica al service
    resultado = update_saldo(db, id, payload)

    # El Route maneja la respuesta HTTP basada en el resultado
    if not resultado:
        raise HTTPException(status_code=404, detail="Saldo bancario no encontrado")

    return resultado
