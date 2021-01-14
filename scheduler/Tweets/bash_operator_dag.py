from configparser import ConfigParser
from datetime import timedelta

from airflow import DAG

from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='Tweets_process_bash_operator',
    default_args=default_args,
    description='A simple DAG',
    schedule_interval='@hourly',
    catchup=False
)

config = ConfigParser()
config.read("/home/pi/test/settings.ini")

script_folder = config['common']['script_folder']
script = f"{script_folder}/start.sh"

if not os.path.exists(script):
    raise Exception("Cannot locate {}".format(script))

t1 = BashOperator(
    task_id='Extraction',
    bash_command=script + " extract ",
    dag=dag
)

t2 = BashOperator(
    task_id='Loading',
    bash_command=script + " load ",
    dag=dag
)

t3 = BashOperator(
    task_id='Projection',
    bash_command=script + " project ",
    dag=dag
)

t4 = BashOperator(
    task_id='Analyzing',
    bash_command=script + " analyze ",
    dag=dag
)

t1 >> t2 >> t3 >> t4
