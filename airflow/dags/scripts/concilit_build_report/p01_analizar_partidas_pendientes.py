from ..utils.engine_db import get_engine_db
from airflow.decorators import task
import pandas as pd
from sqlalchemy import text
import sys, os
from ..p_update_status import update_status_reporte_saldo_bancario


@task(multiple_outputs=True)
def analizar_partidas_pendientes(id_saldo_bancario):
    path_result = os.path.join('/data/results/via_pandas/' + str(id_saldo_bancario) + '.csv')

    try:
        update_status_reporte_saldo_bancario(id_saldo_bancario, 'En proceso - Análisis partidas pendientes vía Pandas')

        if os.path.isfile(path_result):
            os.remove(path_result)

        engine = get_engine_db()

        query = """
            SELECT * FROM fn_asignaciones_analizar_via_pandas(:id_saldo_bancario)
        """
        df_asignaciones_pendientes = pd.read_sql(
            text(query),
            engine,
            params={"id_saldo_bancario": id_saldo_bancario}
        )

        if len(df_asignaciones_pendientes) == 0:
            print('No asignaciones pendientes encontrados')
            return {'id_saldo_bancario': id_saldo_bancario, 'hay_filas': False}

        query = """
                SELECT * \
                FROM fn_partidas_analizar_via_pandas(:id_saldo_bancario) \
                """
        df_partidas_pendientes = pd.read_sql(
            text(query),
            engine,
            params={"id_saldo_bancario": id_saldo_bancario}
        )

        if len(df_partidas_pendientes) == 0 or df_partidas_pendientes.empty:
            return {'id_saldo_bancario': id_saldo_bancario, 'hay_filas': False}

        df_res = process(df_partidas_pendientes)

        df_res.to_csv(path_result, index=False)

        return {'id_saldo_bancario': id_saldo_bancario, 'hay_filas': True}

    except Exception as e:
        update_status_reporte_saldo_bancario(id_saldo_bancario, 'Falló build - Análisis partidas pendientes')
        print(e)
        sys.exit(1)


def process(df_total: pd.DataFrame):
    df_resultado = pd.DataFrame()

    grupos = df_total.groupby('asignacion')

    for nombre, df_grupo in grupos:
        df_nuevo = process_one_asignacion(df_grupo)
        df_resultado = pd.concat([df_resultado, df_nuevo])

    return df_resultado


def process_one_asignacion(df: pd.DataFrame):
    df_positivos = df[df['importe_valorado_ml2'] > 0].copy()
    df_negativos = df[df['importe_valorado_ml2'] < 0].copy()

    df_negativos['asociado'] = None
    df_negativos['asociado'] = df_negativos['asociado'].astype('object')

    df_sub_resultado = []

    for idx_pos, row_pos in df_positivos.iterrows():

        # buscar negativo no asociado que coincida en valor absoluto
        match = df_negativos[
            (df_negativos['asociado'].isna()) &
            (df_negativos['importe_valorado_ml2'] == -row_pos['importe_valorado_ml2'])
        ]

        if not match.empty:
            idx_neg = match.index[0]
            df_negativos.loc[idx_neg, 'asociado'] = row_pos['id_carga_mayor']
        else:
            df_sub_resultado.append(row_pos)

    return pd.DataFrame(df_sub_resultado)
