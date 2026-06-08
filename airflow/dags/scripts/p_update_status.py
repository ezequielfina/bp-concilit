from sqlalchemy import text
from .utils.engine_db import get_engine_db


def update_status_base(query: str, pars: dict):
    stmt = text(query)

    engine = get_engine_db()

    with engine.begin() as db_conn:
        db_conn.execute(stmt, pars)


def update_status_carga_mayor(id_carga_mayor: str, new_status: str):
    query = 'UPDATE cargas_mayor SET estado = :status WHERE id = :id'

    update_status_base(query, {"status": new_status, "id": id_carga_mayor})


def update_status_reporte_saldo_bancario(id_saldo_bancario: str, new_status: str):
    query = 'UPDATE saldos_bancarios SET status_reporte = :status WHERE id = :id'

    update_status_base(query, {"status": new_status, "id": id_saldo_bancario})


def update_extension_reporte_saldo_bancario(id_saldo_bancario: str, extension: str):
    query = 'UPDATE saldos_bancarios SET extension_reporte = :ext WHERE id = :id'

    update_status_base(query, {"ext": extension, "id": id_saldo_bancario})
