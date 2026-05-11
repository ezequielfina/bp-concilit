from airflow.decorators import task
from .utils.engine_db import get_engine
from sqlalchemy import text
import sys


@task
def update_anterior():
    try:
        engine = get_engine()

        with engine.begin() as conn:

            sp_name = 'sp_update_anterior'
            stmt = text(f'CALL {sp_name}()')

            conn.execute(stmt)

    except Exception as e:
        print('Error trying to update anterior: ', e)
        sys.exit(1)
