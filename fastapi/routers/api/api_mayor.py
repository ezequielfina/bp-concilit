from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form
from services.conciliaciones.service_mayor import get_file_mayor_original
from dto.conciliaciones.CargaMayorDTO import CargaMayorCreate, CargaMayorSchema
from dto.conciliaciones.PartidaDTO import PartidaSchema
from utils.engine_db import get_db
from dto.conciliaciones.MayorDTO import MayorSchema, MayorUpdate
from uuid import UUID
from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from services.conciliaciones.service_mayor import read_partidas_by_filtros, update_mayor, save_mayor, read_carga_mayor_by_id, read_cargas_mayor_by_id_cuenta, cambiar_activo_carga_mayor_by_id
from fastapi.responses import FileResponse


api_mayor = APIRouter(prefix="/partidas", tags=["Partidas", "Mayor"])

@api_mayor.get("/", response_model=list[PartidaSchema])
def obtener_partidas_by_filtros(
id_cuenta: UUID,
        asignacion: Optional[str] = None,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        id_carga_mayor: Optional[UUID] = None,
        db: Session = Depends(get_db)
):
    return read_partidas_by_filtros(id_cuenta, asignacion, fecha_inicio, fecha_fin, id_carga_mayor, db)


@api_mayor.get('/download-original-file/{id_carga_mayor}')
def downloaad_file_mayor(id_carga_mayor: UUID):
    path = get_file_mayor_original(str(id_carga_mayor))

    return FileResponse(
        path=path,
        filename=f"{str(id_carga_mayor)}.txt",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@api_mayor.get("/{id_carga_mayor}", response_model=CargaMayorSchema)
def obtener_carga_mayor_by_id(id_carga_mayor: UUID, db: Session = Depends(get_db)):
    return read_carga_mayor_by_id(id_carga_mayor, db)


@api_mayor.get("/cuenta/{id_cuenta}", response_model=list[CargaMayorSchema])
def obtener_carga_mayor_by_id(id_cuenta: UUID, db: Session = Depends(get_db)):
    return read_cargas_mayor_by_id_cuenta(id_cuenta, db)


@api_mayor.put("/{id}", response_model=MayorSchema)
def modificar_partida(partida_data: MayorUpdate, id: UUID, db: Session = Depends(get_db)):
    return update_mayor(partida_data, id, db)


# Cambiamos MayorSchema por CargaMayorSchema (o el que tenga el campo 'activo')
@api_mayor.put("/carga_mayor/cambiar-activo/{id_carga_mayor}", response_model=CargaMayorSchema)
def modificar_partida(id_carga_mayor: UUID, db: Session = Depends(get_db)):
    return cambiar_activo_carga_mayor_by_id(id_carga_mayor, db)


@api_mayor.post("/subir-mayor")
async def guardar_mayor_para_airflow(
    id_cuenta: UUID = Form(...),          # FastAPI lo extrae del FormData
    comentario: str = Form(None),         # FastAPI lo extrae del FormData
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Reconstruimos el esquema para el Service
    carga_mayor_data = CargaMayorCreate(
        id_cuenta=id_cuenta,
        comentario=comentario,
        estado='Pendiente'
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
        path_final = await save_mayor(carga_mayor_data=carga_mayor_data, file=file, db=db)
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
