from uuid import UUID

from dto.conciliaciones.alicuotas.JurisdiccionDTO import JurisdiccionCreate, JurisdiccionSchema
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.engine_db import get_db
from services.conciliaciones.alicuotas.service_jurisdicciones import insert_nueva_jurisdiccion, read_jurisdiccion_by_id, read_all_jurisdicciones



api_jurisdicciones = APIRouter(prefix='/jurisdicciones')


@api_jurisdicciones.post("/", response_model=JurisdiccionSchema)
def nueva_jur(data_jurisdiccion: JurisdiccionCreate, db: Session = Depends(get_db)):
    return insert_nueva_jurisdiccion(data_jurisdiccion, db)


@api_jurisdicciones.get("/", response_model=list[JurisdiccionSchema])
def get_all_jur(db: Session = Depends(get_db)):
    return read_all_jurisdicciones(db)


@api_jurisdicciones.get("/{id}", response_model=JurisdiccionSchema)
def get_jur_by_id(id_jur: UUID, db: Session = Depends(get_db)):
    return read_jurisdiccion_by_id(id_jur, db)
