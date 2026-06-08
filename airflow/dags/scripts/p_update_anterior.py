from airflow.decorators import task
from .utils.engine_db import get_engine_db
from sqlalchemy import text


@task
def update_anterior():
    try:
        engine = get_engine_db()

        with engine.begin() as conn:

            sp_name = 'sp_update_anterior'
            stmt = text(f'CALL {sp_name}()')

            conn.execute(stmt)

    except Exception as e:
        print('Error trying to update anterior: ', e)
        raise


# TESTEAR ESTA RAMA