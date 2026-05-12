# Datos de conexión (airflow-webserver es el nombre del servicio en Docker)
from models.conciliaciones.SaldoBancario import SaldoBancario
import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
import os



async def call_dag_init_data(id_cuenta: str, id_carga_mayor: str):
    try:

        AIRFLOW_API_URL = os.getenv('AIRFLOW_API_URL')
        AUTH = (os.getenv('AUTH_USER_AIRFLOW'), os.getenv('AUTH_PASSWORD_AIRFLOW'))

        dag_id = os.getenv('DAG_ID_INIT_DATA')
        url = f"{AIRFLOW_API_URL}/dags/{dag_id}/dagRuns"

        payload = {
            "conf": {
                "id_cuenta": id_cuenta,
                "file_name": id_carga_mayor
            }
        }

        return await call_airflow(url, payload, AUTH)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


async def call_airflow(url: str, payload: dict, auth):

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, auth=auth)

            if response.status_code == 200:
                return {"status": "success", "airflow_response": response.json()}
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Airflow Error: {response.text}"
                )
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))


async def build_report(id_saldo_bancario: str, db: Session):

    try:
        db_saldo_bancario = db.query(SaldoBancario).where(SaldoBancario.id == id_saldo_bancario).first()

        if not db_saldo_bancario:
            return None

        db_saldo_bancario.status_reporte = 'Pendiente'

        db.commit()
        db.refresh(db_saldo_bancario)

        AIRFLOW_API_URL = os.getenv('AIRFLOW_API_URL')
        AUTH = (os.getenv('AUTH_USER_AIRFLOW'), os.getenv('AUTH_PASSWORD_AIRFLOW'))

        dag_id = os.getenv('DAG_ID_BUILD_REPORT')
        url = f"{AIRFLOW_API_URL}/dags/{dag_id}/dagRuns"

        payload = {
            "conf": {
                "id_saldo_bancario": id_saldo_bancario
            }
        }

        await call_airflow(url, payload, AUTH)

        return db_saldo_bancario

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
