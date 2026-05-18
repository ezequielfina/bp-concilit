from airflow.decorators import task
from .utils.engine_db import get_hook_sql
from sqlalchemy import text
import sys


@task
def update_anterior():
    try:
        hook_sql = get_hook_sql()
        engine = hook_sql.get_sqlalchemy_engine()

        with engine.begin() as conn:

            sp_name = 'sp_update_anterior'
            stmt = text(f'CALL {sp_name}()')

            conn.execute(stmt)

    except Exception as e:
        print('Error trying to update anterior: ', e)
        raise
