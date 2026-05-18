from airflow.providers.postgres.hooks.postgres import PostgresHook


def get_hook_sql() -> PostgresHook:
    hook: PostgresHook = PostgresHook(postgres_conn_id='conn_postgre_db')

    return hook
