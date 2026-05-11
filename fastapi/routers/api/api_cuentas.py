from fastapi import APIRouter
from uuid import UUID
from dto.conciliaciones.CuentaDTO import CuentaSchema, CuentaCreate, CuentaUpdate
from services.conciliaciones.service_cuentas import (
    read_cuentas_by_id_empresa,
    read_cuenta_by_id,
    insert_nueva_cuenta,
    update_nueva_cuenta
)
from fastapi import Depends
from sqlalchemy.orm import Session
from utils.engine_db import get_db # Tu generador de sesión


api_cuentas = APIRouter(prefix="/cuentas", tags=["Conciliaciones"])


@api_cuentas.get("/", response_model=list[CuentaSchema])
def obtener_cuentas_by_id_empresa(id_empresa: UUID, db: Session = Depends(get_db)):
    return read_cuentas_by_id_empresa(id_empresa, db)


@api_cuentas.get("/{id}", response_model=CuentaSchema)
def obtener_cuenta_by_id(id: UUID, db: Session = Depends(get_db)):
    return read_cuenta_by_id(id, db)


@api_cuentas.post("/", response_model=CuentaSchema)
def crear_cuenta_nueva(cuenta_data: CuentaCreate, db: Session = Depends(get_db)):
    return insert_nueva_cuenta(cuenta_data, db)


@api_cuentas.put("/{id}", response_model=CuentaSchema)
def crear_cuenta_nueva(cuenta_data: CuentaUpdate, id: UUID, db: Session = Depends(get_db)):
    return update_nueva_cuenta(cuenta_data, id, db)
