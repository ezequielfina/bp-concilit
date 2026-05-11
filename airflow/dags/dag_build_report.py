from datetime import timedelta, datetime

from airflow import DAG

from scripts.concilit_build_report.p01_analizar_partidas_pendientes import analizar_partidas_pendientes as app
from scripts.concilit_build_report.p02_get_reporte_main import get_reporte_main as grm
from scripts.concilit_build_report.p03_final_report import final_report as fr
from scripts.p_update_anterior import update_anterior


with DAG(
    "concilit-dag-build-report",
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
    description="Data flow of build report",
    schedule=None,
    start_date=datetime(2026, 2, 19),
    catchup=False
) as dag:

    t0_update_anterior = update_anterior()

    partidas_via_pandas = app(
        id_saldo_bancario="{{ dag_run.conf.get('id_saldo_bancario', 'default_value') }}"
    )

    t1_p_v_p = partidas_via_pandas

    t2_report_from_sql = grm(t1_p_v_p)

    t3_fr = fr(t2_report_from_sql)

    t0_update_anterior >> t1_p_v_p

    t1_p_v_p >> t2_report_from_sql >> t3_fr
