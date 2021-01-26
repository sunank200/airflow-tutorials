from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.subdag import SubDagOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy import DummyOperator

from random import uniform
from datetime import datetime

default_args = {
    'start_date': datetime(2020, 1, 1)
}

def _training_model(task_instance):
    accuracy = uniform(0.1, 10.0)
    print(f'model\'s accuracy: {accuracy}')
    # return accuracy
    task_instance.xcom_push(key='model_accuracy',value=accuracy)

def _choose_best_model(task_instance):
    print('choose best model')
    accuracies = task_instance.xcom_pull(key='model_accuracy', task_ids=[
        'processing_tasks.training_model_a',
        'processing_tasks.training_model_b',
        'processing_tasks.training_model_c'
    ])
    for accuracy in accuracies:
        if accuracy > 5:
            return 'accurate' #['accurate','inaccurate']
    return 'inaccurate'
    # print(accuracies)

# def _is_accurate():
#     return('accurate')

with DAG('xcom_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    downloading_data = BashOperator(
        task_id='downloading_data',
        bash_command='sleep 3',
        do_xcom_push=False
    )

    with TaskGroup('processing_tasks') as processing_tasks:
        training_model_a = PythonOperator(
            task_id='training_model_a',
            python_callable=_training_model
        )

        training_model_b = PythonOperator(
            task_id='training_model_b',
            python_callable=_training_model
        )

        training_model_c = PythonOperator(
            task_id='training_model_c',
            python_callable=_training_model
        )

    choose_model = BranchPythonOperator(
        task_id='task_4',
        python_callable=_choose_best_model
    )

    # is_accurate = BranchPythonOperator(
    #     task_id='is_accurate',
    #     python_callable=_is_accurate
    # )

    accurate = DummyOperator(
        task_id='accurate'
    )

    inaccurate = DummyOperator(
        task_id='inaccurate'
    )

    storing = DummyOperator(
        task_id='storing',
        trigger_rule='none_failed_or_skipped'
    )

    downloading_data >> processing_tasks >> choose_model
    choose_model >> [accurate,inaccurate] >> storing