from fastapi import APIRouter
from uuid import UUID
from fastapi import Depends

from services.conciliaciones.service_report import FileService
from utils.engine_db import get_db
from sqlalchemy.orm import Session
from dto.conciliaciones.SaldoBancarioDTO import SaldoBancarioSchema
from services.conciliaciones.service_airflow import build_report
from fastapi.responses import FileResponse


api_reporte = APIRouter(prefix='/reporte', tags=['Reporte'])


@api_reporte.post('/{id_saldo_bancario}', response_model=SaldoBancarioSchema)
async def construir_reporte(id_saldo_bancario: UUID, db: Session = Depends(get_db)):
    return await build_report(str(id_saldo_bancario), db)


def get_file_service():
    return FileService()


@api_reporte.get('/{id_saldo_bancario}')
def get_reporte(id_saldo_bancario: UUID, service: FileService = Depends(get_file_service),
                db: Session = Depends(get_db)):
    # Ahora, si falla, el Service lanza la excepción y no llega a esta línea
    path, extension = service.get_file_path(id_saldo_bancario, db)

    # Si llega acá, es porque todo salió bien
    return FileResponse(
        path=path,
        filename=f"reporte_{id_saldo_bancario}.{extension}",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
