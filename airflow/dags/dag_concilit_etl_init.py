from datetime import timedelta, datetime

from airflow import DAG

from scripts.concilit_etl_init.p01_validator import val
from scripts.concilit_etl_init.p02_transformer import trans
from scripts.concilit_etl_init.p03_mayor_loader import load
from scripts.p_update_anterior import update_anterior


with DAG(
    "concilit-dag",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "retries": 3,
        "retry_delay": timedelta(minutes=10),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'on_skipped_callback': another_function, #or list of functions
        # 'trigger_rule': 'all_success'
    },
    description="Data flow of concilit",
    schedule=None,
    start_date=datetime(2026, 2, 19),
    catchup=False
) as dag:
    # file_info ahora contiene las "promesas" de las llaves del diccionario

    file_info = val(
        file_name="{{ dag_run.conf.get('file_name', 'default_file') }}",
        id_cuenta="{{ dag_run.conf.get('id_cuenta', 'default_id') }}"
    )

    # Accedemos mediante las llaves del diccionario definido en la tarea
    t2_tranformacion = trans(
        file_name=file_info['file_name'],
        id_cuenta=file_info['id_cuenta']
    )

    t3_load_mayor = load(t2_tranformacion)

    t4_update_anterior = update_anterior()

    file_info >> t2_tranformacion >> t3_load_mayor >> t4_update_anterior
