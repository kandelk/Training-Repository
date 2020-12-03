#!/bin/bash

LOCAL_PROJECT_FOLDER="/mnt/e/Projects/sigma/PyhonAnomaly"
DIST_FOLDER="$LOCAL_PROJECT_FOLDER/dist"

cd "$LOCAL_PROJECT_FOLDER"

python3 setup.py bdist_egg

pip3 install -r requirements.txt -t "./deps"
cd ./deps; zip -r "$DIST_FOLDER/deps.zip" "."

MASTER_SSH="pi@192.168.1.100"
SLAVE1_SSH="pi@192.168.1.101"
SLAVE2_SSH="pi@192.168.1.102"

REMOTE_DAG_FOLDER="/home/pi/airflow/dags/"
LOCAL_DAG_FOLDER="$LOCAL_PROJECT_FOLDER/scheduler/Tweets/*"

REMOTE_PROJECT_FOLDER="/home/pi/test"
MASTER_SSH_PROJECT="${MASTER_SSH}:$REMOTE_PROJECT_FOLDER"
SLAVE1_SSH_PROJECT="${SLAVE1_SSH}:$REMOTE_PROJECT_FOLDER"
SLAVE2_SSH_PROJECT="${SLAVE2_SSH}:$REMOTE_PROJECT_FOLDER"

RESOURCES_SCP_SLAVE1_CMD="scp -r $LOCAL_PROJECT_FOLDER/resources/ $SLAVE1_SSH_PROJECT"
eval "$RESOURCES_SCP_SLAVE1_CMD"

RESOURCES_SCP_SLAVE2_CMD="scp -r $LOCAL_PROJECT_FOLDER/resources/ $SLAVE2_SSH_PROJECT"
eval "$RESOURCES_SCP_SLAVE2_CMD"

RESOURCES_SCP_MASTER_CMD="scp -r $LOCAL_PROJECT_FOLDER/resources/ $MASTER_SSH_PROJECT"
eval "$RESOURCES_SCP_MASTER_CMD"

SCRIPTS_SCP_MASTER_CMD="scp -r $LOCAL_PROJECT_FOLDER/scripts/ $MASTER_SSH_PROJECT"
eval "$SCRIPTS_SCP_MASTER_CMD"

SETTINGS_SCP_CMD="scp $LOCAL_PROJECT_FOLDER/sample/settings.ini $MASTER_SSH_PROJECT"
eval "$SETTINGS_SCP_CMD"

DIST_SCP_CMD="scp -r $DIST_FOLDER  $MASTER_SSH_PROJECT"
eval "$DIST_SCP_CMD"

EXTRACTION_PY_SCP_CMD="scp $LOCAL_PROJECT_FOLDER/sample/Tweets/Extraction/extraction.py $MASTER_SSH_PROJECT"
eval "$EXTRACTION_PY_SCP_CMD"

LOADING_PY_SCP_CMD="scp $LOCAL_PROJECT_FOLDER/sample/Tweets/Loading/loading.py $MASTER_SSH_PROJECT"
eval "$LOADING_PY_SCP_CMD"

PROJECTION_PY_SCP_CMD="scp $LOCAL_PROJECT_FOLDER/sample/Tweets/Projection/projection.py $MASTER_SSH_PROJECT"
eval "$PROJECTION_PY_SCP_CMD"

ANALYSIS_PY_SCP_CMD="scp $LOCAL_PROJECT_FOLDER/sample/Tweets/Analysis/analysis.py $MASTER_SSH_PROJECT"
eval "$ANALYSIS_PY_SCP_CMD"

DAG_SCP_CMD="scp $LOCAL_DAG_FOLDER $MASTER_SSH:$REMOTE_DAG_FOLDER"
eval "$DAG_SCP_CMD"