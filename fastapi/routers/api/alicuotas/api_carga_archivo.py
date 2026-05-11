from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from dto.conciliaciones.alicuotas.CargaAlicuotaDTO import CargaAlicuotaCreate
from services.conciliaciones.alicuotas.service_carga_alicuota import save_archivo_carga_alicuota
from utils.engine_db import get_db

api_carga_archivo = APIRouter(prefix='/carga-archivo', tags=['carga-archivo'])


@api_carga_archivo.post('/')
async def guardar_archivo_alicuota_para_airflow(
    id_empresa: UUID = Form(...),          # FastAPI lo extrae del FormData
    id_jurisdiccion: UUID = Form(...),          # FastAPI lo extrae del FormData
    comentario: str = Form(None),         # FastAPI lo extrae del FormData
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Reconstruimos el esquema para el Service
    carga_mayor_data = CargaAlicuotaCreate(
        id_empresa=id_empresa,
        id_jurisdiccion=id_jurisdiccion,
        comentario=comentario
    )
    # 1. Validación de extensiones
    extension = file.filename.split(".")[-1].lower()
    if extension not in ["txt", "csv"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de archivo no soportado. Use CSV o Excel."
        )

    # 2. Delegar el guardado al Service
    try:
        path_final = await save_archivo_carga_alicuota(data_archivo=carga_mayor_data, file=file, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    finally:
        # Siempre cerramos el archivo para liberar memoria/recursos
        await file.close()

    return {
        "status": "success",
        "message": "Archivo recibido",
        "file_path": path_final
    }
