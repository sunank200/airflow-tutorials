from airflow.models import DAG
from airflow.operators.bash import BashOperator

from datetime import datetime

default_args = {
    'start_date':datetime(2021,1,1)
}

with DAG('trigger_rule',schedule_interval='@daily',default_args=default_args,catchup=False) as dags:
    task_1 = BashOperator(
        task_id='task_1',
        bash_command='exit 1',
        do_xcom_push=False
    )

    task_2 = BashOperator(
        task_id='task_2',
        bash_command='exit 0',
        do_xcom_push=False
    )

    task_3 = BashOperator(
        task_id='task_3',
        bash_command='exit 0',
        do_xcom_push=False,
        trigger_rule='all_done'
    )

    [task_1, task_2] >> task_3