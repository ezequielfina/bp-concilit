import sys

import pandas as pd
import os
from airflow.decorators import task
from ..p_update_status import update_status_reporte_saldo_bancario, update_extension_reporte_saldo_bancario


@task
def final_report(info_previa: dict):
    id_saldo_bancario = info_previa['id_saldo_bancario']

    try:
        update_status_reporte_saldo_bancario(id_saldo_bancario, 'En proceso - Combinando resultados')

        hay_filas = info_previa['hay_filas']

        path_result = os.path.join('/data/results/', id_saldo_bancario + '.xlsx')
        if os.path.isfile(path_result):
            os.remove(path_result)

        path_sql = os.path.join('/data/results/via_sql/', id_saldo_bancario + '.csv')
        df_sql = pd.read_csv(path_sql)

        if hay_filas:
            path_pandas = os.path.join('/data/results/via_pandas/', id_saldo_bancario + '.csv')
            df_pandas = pd.read_csv(path_pandas)

            df = pd.concat([df_sql, df_pandas], ignore_index=True)

            df.to_excel(path_result, index=False)

            update_status_reporte_saldo_bancario(id_saldo_bancario, 'Construcción exitosa')
            update_extension_reporte_saldo_bancario(id_saldo_bancario, '.xlsx')
            return path_result

        df_sql.to_excel(path_result, index=False)

        update_status_reporte_saldo_bancario(id_saldo_bancario, 'Construcción exitosa')
        update_extension_reporte_saldo_bancario(id_saldo_bancario, '.xlsx')
        return path_result

    except Exception as e:
        update_status_reporte_saldo_bancario(id_saldo_bancario, 'Falló build - Combinando resultados')
        print(e)
        sys.exit(1)
