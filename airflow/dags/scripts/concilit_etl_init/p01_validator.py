import pandas as pd
import os
import shutil

from airflow.decorators import task
from ..p_update_status import update_status_carga_mayor


@task(multiple_outputs=True)
def val(file_name: str, id_cuenta: str):
    full_path: str = os.path.join('/data/landing/', file_name + '.txt')

    try:
        update_status_carga_mayor(file_name, 'Validando')

        if not os.path.exists(full_path):
            update_status_carga_mayor(file_name, 'Falló validación - File cause')
            raise FileNotFoundError(f'File not founded, route: {full_path}')

        # Leer archivo
        df_mayor: pd.DataFrame = pd.read_csv(full_path, header=0, sep='\t', encoding='latin1')

        # 1. Limpieza básica de nombres de columnas
        df_mayor.columns = df_mayor.columns.str.strip()

        # 2. Definir el diccionario de Alias (Variación: Nombre Estándar)
        # Aquí agregas todas las formas posibles en que puede venir una columna
        column_aliases = {
            'fecha contabiliz.': 'Fe.contabilización',
            'fe.contabilización': 'Fe.contabilización',
            'f.contabilizacion': 'Fe.contabilización',
            'ejercicio/mes': 'Ejercicio / mes',
            'nro documento': 'Nº documento',
            'nº documento': 'Nº documento',
            'importe moneda doc': 'Importe en moneda doc.',
            'importe en moneda doc.': 'Importe en moneda doc.'
        }

        # 3. Normalizar columnas: Renombrar si el nombre existe en nuestro diccionario de alias
        # Convertimos a minúsculas para una comparación más robusta (opcional)
        new_columns = []
        for col in df_mayor.columns:
            # Buscamos si la columna actual tiene un estándar definido
            standard_name = column_aliases.get(col.lower(), col)
            new_columns.append(standard_name)

        df_mayor.columns = new_columns

        # 4. Lista de columnas finales requeridas (ya normalizadas)
        necessary_columns: list[str] = [
            'Sociedad',
            'Cuenta de mayor',
            'Asignación',
            'Nº documento',
            'Ejercicio / mes',
            'Clase de documento',
            'Fecha de documento',
            'Fe.contabilización',
            'Clave contabiliz.',
            'Importe en moneda doc.',
            'Moneda del documento',
            'Importe en moneda local',
            'Moneda local',
            'Texto cab.documento',
            'Texto',
            'Cta.contrapartida',
            'Referencia',
            'Importe valorado ML2'
        ]

        # 5. Validar si faltan columnas después del renombrado
        missing_columns: set = set(necessary_columns) - set(df_mayor.columns)
        if missing_columns:
            update_status_carga_mayor(file_name, 'Falló validación - Column cause')
            raise ValueError(f'Missing columns (after normalization): {missing_columns}')

        if len(df_mayor) < 1:
            raise ValueError('No rows to process.')

        # Guardar el CSV con las columnas ya normalizadas
        df_path_destino: str = os.path.join('/data/to_transform/', file_name + '.csv')
        df_mayor.to_csv(df_path_destino, index=False)

        destino_source_snapshot: str = '/data/source-snapshot/'
        if not os.path.exists(destino_source_snapshot):
            os.makedirs(destino_source_snapshot)

        shutil.move(full_path, destino_source_snapshot)

        return {
            'file_name': file_name,
            'id_cuenta': id_cuenta
        }

    except FileNotFoundError as e:
        update_status_carga_mayor(file_name, 'Falló validación - File cause')
        print(f'Error in the path -> {e}')
        raise
    except ValueError as e:
        update_status_carga_mayor(file_name, 'Falló validación')
        print(f'Error in data -> {e}')
        raise
    except Exception as e:
        update_status_carga_mayor(file_name, 'Falló validación')
        print('Error trying to validate original file: ', e)
        raise
