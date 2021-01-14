from configparser import ConfigParser
from datetime import timedelta

from airflow import DAG

from airflow.contrib.operators.aws_athena_operator import AWSAthenaOperator
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
    dag_id='Tweets_process__aws_athena_operator',
    default_args=default_args,
    description='A simple DAG',
    schedule_interval='@hourly',
    catchup=False
)

t1 = AWSAthenaOperator(
        task_id='run_query',
        query='SELECT * FROM tweet',
        output_location='s3://project.tweet.query.results/test/',
        database='default'
    )

t1
