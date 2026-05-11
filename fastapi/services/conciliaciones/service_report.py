import os
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.conciliaciones.SaldoBancario import SaldoBancario


# Asegurate de importar tu modelo SaldoBancario

class FileService:
    def get_file_path(self, id_saldo_bancario: UUID, db: Session):
        try:
            # 1. Buscar en la base de datos
            db_saldo_bancario = db.query(SaldoBancario).where(SaldoBancario.id == id_saldo_bancario).first()

            if not db_saldo_bancario:
                raise HTTPException(status_code=404, detail="Registro de saldo no encontrado.")

            # 2. Normalizar el status para comparar (chau tildes y mayúsculas)
            # Esto hace que "Construcción exitosa" sea igual a "construccion exitosa"
            status_normalizado = db_saldo_bancario.status_reporte.lower().replace('ó', 'o').strip()

            if status_normalizado != 'construccion exitosa':
                raise HTTPException(
                    status_code=400,
                    detail=f"El reporte aún no está listo. Estado actual: {db_saldo_bancario.status_reporte}"
                )

            # 3. Validar extensión
            if not db_saldo_bancario.extension_reporte:
                raise HTTPException(status_code=400, detail="El registro no tiene una extensión de archivo definida.")

            # 4. Construir el path (limpiando el punto por si las dudas)
            base_path = "/data/results/"
            extension = db_saldo_bancario.extension_reporte.replace('.', '')
            file_name = f"{str(id_saldo_bancario)}.{extension}"
            file_path = os.path.join(base_path, file_name)

            # 5. Verificar si el archivo realmente existe en el volumen /data
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404,
                    detail=f"Archivo físico no encontrado en el servidor: {file_name}"
                )

            # Si todo está OK, devolvemos la tupla
            return file_path, extension

        except HTTPException as he:
            # Re-lanzamos las excepciones controladas de FastAPI
            raise he
        except Exception as e:
            # Capturamos cualquier otro error inesperado (DB caída, permisos, etc.)
            print(f"Error crítico en FileService: {str(e)}")
            raise HTTPException(status_code=500, detail="Error interno al procesar el archivo.")