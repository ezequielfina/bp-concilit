from airflow.models.connection import Connection
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy import create_engine


def get_hook_sql() -> PostgresHook:
    hook: PostgresHook = PostgresHook(postgres_conn_id='conn_postgre_db')

    return hook


def get_engine_db():
    hook_sql = get_hook_sql()

    conn: Connection = hook_sql.get_connection('conn_postgre_db')

    uri = f"postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"

    return create_engine(uri)
