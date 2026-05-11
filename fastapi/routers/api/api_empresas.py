from fastapi import APIRouter
from uuid import UUID
from dto.EmpresaDTO import EmpresaSchema, EmpresaCreate, EmpresaUpdate
from fastapi import Depends
from sqlalchemy.orm import Session
from utils.engine_db import get_db # Tu generador de sesión
from services.ser_empresas import read_empresas, read_empresa_by_id, insert_empresa, update_empresa


api_empresas = APIRouter(prefix="/empresas", tags=["Empresas"])


@api_empresas.get("/", response_model=list[EmpresaSchema])
def get_empresas_json(db: Session = Depends(get_db)):
    return read_empresas(db)


@api_empresas.get("/{id}", response_model=EmpresaSchema)
def get_empresa_by_id_json(id: UUID, db: Session = Depends(get_db)):
    return read_empresa_by_id(id, db)


@api_empresas.post("/", response_model=EmpresaSchema)
def crear_nueva_empresa(data_empresa: EmpresaCreate, db: Session = Depends(get_db)):
    return insert_empresa(data_empresa, db)


@api_empresas.put("/{id}", response_model=EmpresaSchema)
def modificar_nueva_empresa(data_empresa: EmpresaUpdate, id: UUID, db: Session = Depends(get_db)):
    return update_empresa(data_empresa, id, db)
