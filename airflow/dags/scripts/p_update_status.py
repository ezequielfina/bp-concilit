from sqlalchemy import text
from .utils.engine_db import get_engine


def update_status_carga_mayor(id_carga_mayor: str, new_status: str):
    engine = get_engine()

    stmt = text('UPDATE cargas_mayor SET estado = :status WHERE id = :id')

    with engine.begin() as conn:
        conn.execute(stmt, {"status": new_status, "id": id_carga_mayor})


def update_status_reporte_saldo_bancario(id_saldo_bancario: str, new_status: str):
    engine = get_engine()

    stmt = text('UPDATE saldos_bancarios SET status_reporte = :status WHERE id = :id')

    with engine.begin() as conn:
        conn.execute(stmt, {"status": new_status, "id": id_saldo_bancario})


def update_extension_reporte_saldo_bancario(id_saldo_bancario: str, extension: str):
    engine = get_engine()

    stmt = text('UPDATE saldos_bancarios SET extension_reporte = :ext WHERE id = :id')

    with engine.begin() as conn:
        conn.execute(stmt, {"ext": extension, "id": id_saldo_bancario})
