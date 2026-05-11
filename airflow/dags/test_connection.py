from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def print_params(**context):
    # 'conf' es donde Airflow guarda lo que enviamos desde la API
    message = context['dag_run'].conf.get('message', 'No llegó nada')
    print(f"Mensaje recibido desde FastAPI: {message}")

with DAG(
    dag_id='test_fastapi_connection',
    start_date=datetime(2026, 1, 1),
    schedule_interval=None, # Solo se dispara por API
    catchup=False
) as dag:

    test_task = PythonOperator(
        task_id='print_fastapi_message',
        python_callable=print_params,
    )