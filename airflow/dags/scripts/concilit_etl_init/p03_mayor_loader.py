import os
import pandas as pd
from airflow.decorators import task
from ..p_update_status import update_status_carga_mayor
from ..utils.engine_db import get_engine_db


@task
def load(file_name):

    try:
        update_status_carga_mayor(file_name, 'Cargando data en DB')

        engine = get_engine_db()

        full_path = os.path.join('/data/to_load/mayor', file_name + '.csv')
        df_mayor: pd.DataFrame = pd.read_csv(full_path)

        columnas: list[str] = [
            'sociedad',
            'cuenta',
            'asignacion',
            'documento',
            'clase_doc',
            'clave_contabilizacion',
            'importe_moneda_doc',
            'moneda_doc',
            'importe_moneda_local',
            'moneda_local',
            'texto_cab_doc',
            'texto',
            'cuenta_contrapartida',
            'referencia',
            'importe_valorado_ml2',
            'ejercicio_mes',
            'fecha_doc',
            'fecha_contabilizacion',
            'id_cuenta',
            'id_carga_mayor'
        ]

        df_mayor[columnas].to_sql('mayor', engine, index=False, if_exists='append')

        update_status_carga_mayor(file_name, 'Carga exitosa')

        import shutil

        destino: str = '/data/loaded/mayor/'
        shutil.move(full_path, destino)

    except FileNotFoundError as e:
        update_status_carga_mayor(file_name, 'Falló carga en DB - File cause')
        print(f'Error in the path -> {e}')
        raise

    except ValueError as e:
        update_status_carga_mayor(file_name, 'Falló carga en DB')
        print(f'Error in data -> {e}')
        raise

    except Exception as e:
        update_status_carga_mayor(file_name, 'Falló carga en DB')
        print('Error trying to validate original file: ', e)
        raise