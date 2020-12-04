from configparser import ConfigParser
from datetime import timedelta

from airflow import DAG

from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
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
    dag_id='Tweets_process_spark_operator',
    default_args=default_args,
    description='A simple DAG',
    schedule_interval='@hourly',
    catchup=False
)

config = ConfigParser()
config.read("/home/pi/test/settings.ini")

project_folder = config['common']['project_folder']
dist_folder = config['common']['dist_folder']

_config ={
    'master': config['spark']['remote'],
    'executor_memory': '512m',
    'py_files': f"{dist_folder}/Anomaly-0.1-py3.8.egg,{dist_folder}/deps.zip",
    'jars': f"{dist_folder}/postgresql-42.2.8.jar",
    'driver_class_path': f"{dist_folder}/postgresql-42.2.8.jar"
}

extraction_py = f"{project_folder}/extraction.py"
if os.path.exists(extraction_py):
    t1 = SparkSubmitOperator(
        task_id='Extraction',
        application=extraction_py,
        dag=dag,
        **_config
    )
else:
    raise Exception("Cannot locate {}".format(extraction_py))

loading_py = f"{project_folder}/loading.py"
if os.path.exists(loading_py):
    t2 = SparkSubmitOperator(
        task_id='Loading',
        application=loading_py,
        dag=dag,
        **_config
    )
else:
    raise Exception("Cannot locate {}".format(loading_py))

projection_py = f"{project_folder}/projection.py"
if os.path.exists(projection_py):
    t3 = SparkSubmitOperator(
        task_id='Projection',
        application=projection_py,
        dag=dag,
        **_config
    )
else:
    raise Exception("Cannot locate {}".format(projection_py))

analysis_py = f"{project_folder}/analysis.py"
if os.path.exists(analysis_py):
    t4 = SparkSubmitOperator(
        task_id='Analysis',
        application=analysis_py,
        dag=dag,
        **_config
    )
else:
    raise Exception("Cannot locate {}".format(analysis_py))

t1 >> t2 >> t3 >> t4
