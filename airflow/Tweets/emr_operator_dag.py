from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor
from datetime import timedelta

from airflow import DAG

from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(seconds=10),
}

dag = DAG(
    dag_id='Emr_operator',
    default_args=default_args,
    description='A simple DAG',
    schedule_interval=None,
    catchup=False
)

cluster_id = "j-2XMW33C5GSKO6"

# Buckets
BUCKET_NAME = "s3://project.tweet.functions"
RESULT_BUCKET_NAME = "s3://project.tweet.kramatorsk.projection"

# Scripts
extraction = f"{BUCKET_NAME}/scripts/extraction.py"
loading = f"{BUCKET_NAME}/scripts/loading.py"
projection = f"{BUCKET_NAME}/scripts/projection.py"
analysis = f"{BUCKET_NAME}/scripts/analysis.py"

# Resources
deps = f"{BUCKET_NAME}/resources/deps.zip"
egg_project = f"{BUCKET_NAME}/resources/Anomaly-0.1-py3.8.egg"
postgre_driver = f"{BUCKET_NAME}/resources/postgresql-42.2.8.jar"

EMR_STEPS = [
    {
        "Name": "{{ params.name }}",
        "ActionOnFailure": "CANCEL_AND_WAIT",
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": [
                "spark-submit",
                "--jars", "{{ params.postgre_driver }}",
                "--py-files", "{{ params.egg_project }}",
                "{{ params.s3_script }}",
            ],
        },
    }
]

Extraction = EmrAddStepsOperator(
    task_id="Extraction",
    job_flow_id=cluster_id,
    aws_conn_id="aws_default",
    steps=EMR_STEPS,
    params={
        "s3_script": extraction,
        "postgre_driver": postgre_driver,
        "egg_project": egg_project,
        "name": "Extraction"
    },
    dag=dag,
)

last_step = len(EMR_STEPS) - 1
Check_extraction = EmrStepSensor(
    task_id="watch_extraction",
    job_flow_id=cluster_id,
    step_id="{{ task_instance.xcom_pull(task_ids='Extraction', key='return_value')["
            + str(last_step)
            + "] }}",
    aws_conn_id="aws_default",
    dag=dag,
)

Loading = EmrAddStepsOperator(
    task_id="Loading",
    job_flow_id=cluster_id,
    aws_conn_id="aws_default",
    steps=EMR_STEPS,
    params={
        "s3_script": loading,
        "postgre_driver": postgre_driver,
        "egg_project": egg_project,
        "name": "Loading"
    },
    dag=dag,
)

last_step = len(EMR_STEPS) - 1
Check_loading = EmrStepSensor(
    task_id="watch_loading",
    job_flow_id=cluster_id,
    step_id="{{ task_instance.xcom_pull(task_ids='Loading', key='return_value')["
            + str(last_step)
            + "] }}",
    aws_conn_id="aws_default",
    dag=dag,
)

Projection = EmrAddStepsOperator(
    task_id="Projection",
    job_flow_id=cluster_id,
    aws_conn_id="aws_default",
    steps=EMR_STEPS,
    params={
        "s3_script": projection,
        "postgre_driver": postgre_driver,
        "egg_project": egg_project,
        "name": "Projection"
    },
    dag=dag,
)

last_step = len(EMR_STEPS) - 1
Check_projection = EmrStepSensor(
    task_id="watch_projection",
    job_flow_id=cluster_id,
    step_id="{{ task_instance.xcom_pull(task_ids='Projection', key='return_value')["
            + str(last_step)
            + "] }}",
    aws_conn_id="aws_default",
    dag=dag,
)

Analysis = EmrAddStepsOperator(
    task_id="Analysis",
    job_flow_id=cluster_id,
    aws_conn_id="aws_default",
    steps=EMR_STEPS,
    params={
        "s3_script": analysis,
        "postgre_driver": postgre_driver,
        "egg_project": egg_project,
        "name": "Analysis"
    },
    dag=dag,
)

last_step = len(EMR_STEPS) - 1
Check_analysis = EmrStepSensor(
    task_id="watch_analysis",
    job_flow_id=cluster_id,
    step_id="{{ task_instance.xcom_pull(task_ids='Analysis', key='return_value')["
            + str(last_step)
            + "] }}",
    aws_conn_id="aws_default",
    dag=dag,
)

Extraction >> Check_extraction >> Loading >> Check_loading >> Projection >> Check_projection >> Analysis >> Check_analysis
