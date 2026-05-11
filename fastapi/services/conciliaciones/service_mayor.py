import os
import shutil
from uuid import UUID
from datetime import date
from typing import Optional
from fastapi import UploadFile, HTTPException
from models.conciliaciones.Mayor import Mayor
from models.conciliaciones.Cuenta import Cuenta
from models.conciliaciones.CargaMayor import CargaMayor
from models.conciliaciones.VW_Partida import VWPartida
from sqlalchemy.orm import Session
from sqlalchemy import select
from dto.conciliaciones.MayorDTO import MayorUpdate
from dto.conciliaciones.CargaMayorDTO import CargaMayorCreate
from .service_airflow import call_dag_init_data


def read_partidas_by_filtros(
        id_cuenta: UUID,
        asignacion: Optional[str],
        fecha_inicio: Optional[date],
        fecha_fin: Optional[date],
        id_carga_mayor: UUID,
        db: Session
):
    # 1. Iniciamos la base del select
    stmt = select(VWPartida).where(VWPartida.id_cuenta == id_cuenta)

    # 2. Añadimos filtros condicionales
    if asignacion:
        # Usamos ilike para que no importe mayúsculas/minúsculas
        stmt = stmt.where(VWPartida.asignacion.ilike(f"%{asignacion}%"))

    if fecha_inicio:
        stmt = stmt.where(VWPartida.fecha_doc >= fecha_inicio)

    if fecha_fin:
        stmt = stmt.where(VWPartida.fecha_doc <= fecha_fin)

    if id_carga_mayor:
        stmt = stmt.where(VWPartida.id_carga_mayor == id_carga_mayor)

    # 3. Ordenamos (opcional, pero recomendado en finanzas/logística)
    stmt = stmt.order_by(VWPartida.fecha_doc.desc())

    # 4. Ejecutamos y retornamos los resultados
    result = db.execute(stmt)
    return result.scalars().all()


def read_cargas_mayor_by_id_cuenta(id_cuenta: UUID, db: Session):
    stmt = select(CargaMayor).where(CargaMayor.id_cuenta == id_cuenta)

    result = db.execute(stmt)

    return result.scalars().all()


def read_carga_mayor_by_id(id_carga_mayor: UUID, db: Session):
    return db.query(CargaMayor).where(CargaMayor.id == id_carga_mayor).first()


def cambiar_activo_carga_mayor_by_id(id: UUID, db: Session):
    db_carga_mayor = db.query(CargaMayor).where(CargaMayor.id == id).first()

    if not db_carga_mayor:
        return None

    db_carga_mayor.activo = not db_carga_mayor.activo

    db.commit()

    db.refresh(db_carga_mayor)

    return db_carga_mayor


def get_file_mayor_original(id_carga_mayor: str):
    base_path = '/data/source-snapshot/'
    file_path = id_carga_mayor + '.txt'

    path = os.path.join(base_path, file_path)

    if not os.path.exists(path):
        print(f'File not founded', file_path)

        raise HTTPException(
            status_code=404,
            detail=f"Archivo físico no encontrado en el servidor: {file_path}"
        )

    return path


def update_mayor(mayor_data: MayorUpdate, id: UUID, db: Session):
    db_mayor = db.query(Mayor).where(Mayor.id == id).first()

    if not db_mayor:
        return None

    update_data = mayor_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_mayor, key, value)

    db.commit()
    db.refresh(db_mayor)

    return db_mayor


async def save_mayor(carga_mayor_data: CargaMayorCreate, file: UploadFile, db: Session):
    carga_mayor: Optional[CargaMayor] = save_carga_mayor(carga_mayor_data, db)

    if not carga_mayor:
        return None

    id_carga_mayor: str = save_file_to_disk(file, str(carga_mayor.id))

    return await call_dag_init_data(str(carga_mayor.id_cuenta), str(id_carga_mayor))


def save_carga_mayor(carga_mayor_data: CargaMayorCreate, db: Session):
    cuenta = db.query(Cuenta).where(Cuenta.id == carga_mayor_data.id_cuenta).first()

    if not cuenta:
        return None

    new_carga = CargaMayor(
        id_cuenta=carga_mayor_data.id_cuenta,
        comentario=carga_mayor_data.comentario,
        estado="Pendiente",
        activo=True
    )

    db.add(new_carga)
    db.commit()

    db.refresh(new_carga)

    return new_carga


def save_file_to_disk(file: UploadFile, new_file_name: str) -> str:
    # 1. Definimos el directorio
    UPLOAD_DIR = "/data/landing"

    # 2. CREAR LA CARPETA SI NO EXISTE (Esto soluciona tu error Errno 2)
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    # 3. Definimos la ruta completa del archivo
    ruta_destino = os.path.join(UPLOAD_DIR, new_file_name + '.txt')

    try:
        # Usamos file.file para obtener el objeto compatible con copyfileobj
        with open(ruta_destino, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise Exception(f"Error fatal al guardar: {str(e)}")

    return new_file_name


def read_mayor_by_filtros(
        id_cuenta: UUID,
        asignacion: Optional[str],
        fecha_inicio: Optional[date],
        fecha_fin: Optional[date],
        id_carga_mayor: UUID,
        db: Session
):

    stmt = select(Mayor).where(Mayor.id_cuenta == id_cuenta)

    # 2. Añadimos filtros condicionales
    if asignacion:
        # Usamos ilike para que no importe mayúsculas/minúsculas
        stmt = stmt.where(Mayor.asignacion.ilike(f"%{asignacion}%"))

    if fecha_inicio:
        stmt = stmt.where(Mayor.fecha_doc >= fecha_inicio)

    if fecha_fin:
        stmt = stmt.where(Mayor.fecha_doc <= fecha_fin)

    if id_carga_mayor:
        stmt = stmt.where(Mayor.id_carga_mayor == id_carga_mayor)

    # 3. Ordenamos (opcional, pero recomendado en finanzas/logística)
    stmt = stmt.order_by(Mayor.fecha_doc.desc())

    # 4. Ejecutamos y retornamos los resultados
    result = db.execute(stmt)
    return result.scalars().all()
