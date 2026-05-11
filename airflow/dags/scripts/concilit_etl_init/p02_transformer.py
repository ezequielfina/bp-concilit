import os
import sys
import pandas as pd
from airflow.decorators import task
from ..p_update_status import update_status_carga_mayor


@task
def trans(file_name, id_cuenta: str):
    try:
        update_status_carga_mayor(file_name, 'Transformando')
        full_path = os.path.join('/data/to_transform/', file_name + '.csv')

        if not os.path.exists(full_path):
            update_status_carga_mayor(file_name, 'Falló transformación - File cause')
            raise FileNotFoundError(f'File not founded, route: {full_path}')

        dtypes_iniciales = {
            'Sociedad': str,
            'Cuenta de mayor': str,
            'Nº documento': str,
            'Ejercicio / mes': str,
            'Clave contabiliz.': str,
            'Cta.contrapartida': str,
            'Referencia': str
        }

        # Leemos el CSV forzando los tipos definidos arriba
        df_mayor: pd.DataFrame = pd.read_csv(full_path, dtype=dtypes_iniciales)
        # ------------------------------

        # Normalización de nombres de columnas
        df_mayor.columns = df_mayor.columns.str.strip().str.lower().str.replace(' ', '_')

        df_mayor['id_cuenta'] = id_cuenta
        df_mayor['id_carga_mayor'] = file_name

        df_mayor.rename(columns={
            'cuenta_de_mayor': 'cuenta',
            'asignación': 'asignacion',
            'nº_documento': 'documento',
            'ejercicio_/_mes': 'ejercicio_mes',
            'clase_de_documento': 'clase_doc',
            'fecha_de_documento': 'fecha_doc',
            'fe.contabilización': 'fecha_contabilizacion',
            'clave_contabiliz.': 'clave_contabilizacion',
            'importe_en_moneda_doc.': 'importe_moneda_doc',
            'moneda_del_documento': 'moneda_doc',
            'importe_en_moneda_local': 'importe_moneda_local',
            'moneda_local': 'moneda_local',
            'texto_cab.documento': 'texto_cab_doc',
            'cta.contrapartida': 'cuenta_contrapartida'
        }, inplace=True)

        types: dict = {
            'sociedad': str,
            'cuenta': str,
            'asignacion': str,
            'documento': str,
            'clase_doc': str,
            'clave_contabilizacion': str,
            'importe_moneda_doc': float,
            'moneda_doc': str,
            'importe_moneda_local': float,
            'moneda_local': str,
            'texto_cab_doc': str,
            'texto': str,
            'cuenta_contrapartida': str,
            'referencia': str,
            'importe_valorado_ml2': float
        }

        cols_numericas = [
            'importe_moneda_doc',
            'importe_moneda_local',
            'importe_valorado_ml2'
        ]

        for col in cols_numericas:
            # Si ya es numérico (porque no tenía separadores), lo pasamos a str para limpiar
            df_mayor[col] = (
                df_mayor[col]
                .astype(str)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
            )

        # Ahora el astype(types) funcionará sin problemas en las columnas de texto
        df_mayor = df_mayor.astype(types)

        df_mayor['ejercicio_mes'] = pd.to_datetime(df_mayor['ejercicio_mes'], format='%Y/%m')
        df_mayor['fecha_doc'] = pd.to_datetime(df_mayor['fecha_doc'], format='%d/%m/%Y')
        df_mayor['fecha_contabilizacion'] = pd.to_datetime(df_mayor['fecha_contabilizacion'], format='%d/%m/%Y')

        df_mayor['id_periodo'] = file_name.replace('.csv', '')

        destino: str = '/data/to_load/mayor'
        if not os.path.exists(destino):
            os.makedirs(destino)

        destino = os.path.join(destino, file_name + '.csv')
        df_mayor.to_csv(destino, index=False)

        os.remove(full_path)

        return file_name

    except Exception as e:
        update_status_carga_mayor(file_name, 'Falló transformación')
        print('Error trying to transform file: ', e)
        sys.exit(1)
