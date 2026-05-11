import shutil
from typing import Optional
import os
from sqlalchemy.orm import Session
from fastapi import UploadFile

from dto.conciliaciones.alicuotas.CargaAlicuotaDTO import CargaAlicuotaCreate
from models.Empresa import Empresa
from models.conciliaciones.alicuotas.CargaAlicuota import CargaAlicuota
from models.conciliaciones.alicuotas.Jurisdiccion import Jurisdiccion
from services.conciliaciones.alicuotas.service_airflow import call_dag_init_data_ali


async def save_archivo_carga_alicuota(data_archivo: CargaAlicuotaCreate, file: UploadFile, db: Session):
    id_carga_alicuota: Optional[str] = save_carga_alicuota(data_archivo, db)

    if id_carga_alicuota is None:
        return None

    id_carga_alicuota = save_file_to_disk(file, id_carga_alicuota)

    return call_dag_init_data_ali(id_carga_alicuota)


def save_carga_alicuota(data_archivo: CargaAlicuotaCreate, db: Session):
    empresa: Optional[CargaAlicuota] = db.query(Empresa).where(Empresa.id == data_archivo.id_empresa).first()

    jurisdiccion: Optional[CargaAlicuota] = db.query(Jurisdiccion).where(Jurisdiccion.id == data_archivo.id_jurisdiccion).first()

    if empresa is None or jurisdiccion is None:
        return None

    carga_alicuota = CargaAlicuota(
        id_empresa=data_archivo.id_empresa,
        id_jurisdiccion=data_archivo.id_jurisdiccion,
        comentario=data_archivo.comentario
    )

    db.add(carga_alicuota)
    db.commit()

    db.refresh(carga_alicuota)

    return str(carga_alicuota.id)


def save_file_to_disk(file: UploadFile, new_file_name: str) -> str:
    # 1. Definimos el directorio
    UPLOAD_DIR = "/data/conciliaciones/alicuotas/landing"

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
