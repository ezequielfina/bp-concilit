import os

from ..utils.engine_db import get_hook_sql
from airflow.decorators import task
import pandas as pd
from sqlalchemy import text
from ..p_update_status import update_status_reporte_saldo_bancario


@task
def get_reporte_main(info_previa: dict):
    id_saldo_bancario = info_previa['id_saldo_bancario']
    try:

        update_status_reporte_saldo_bancario(id_saldo_bancario, 'En proceso - Analizando partidas pendientes vía SQL')

        hay_filas = info_previa['hay_filas']
        path_result = os.path.join('/data/results/via_sql/' + str(id_saldo_bancario) + '.csv')

        if os.path.isfile(path_result):
            os.remove(path_result)


        hook_sql = get_hook_sql()
        engine = hook_sql.get_sqlalchemy_engine()
        query = """
        SELECT * FROM fn_previo_partidas_pendientes(:id_saldo_bancario)
        """

        df = pd.read_sql(text(query), con=engine, params={"id_saldo_bancario": id_saldo_bancario})

        df.to_csv(path_result, index=False)

        return {'id_saldo_bancario': id_saldo_bancario, 'hay_filas': hay_filas}

    except Exception as e:
        update_status_reporte_saldo_bancario(id_saldo_bancario, 'Falló build - Analizando partidas pendientes vía SQL')
        print(e)
        raise
