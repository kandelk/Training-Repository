#!/bin/bash
python3 setup.py bdist_egg

if ! command -v pipreqs &> /dev/null
then
    pip3 install pipreqs
fi
pipreqs

pip3 install -r requirements.txt -t ./deps
zip -r dist/deps.zip ./deps

PROJECT_EGG="./dist/Anomaly-0.1-py3.8.egg"
SPARK_CMD="spark-submit --master yarn --py-files $PROJECT_EGG,dist/deps.zip build/lib/sample/__init__.py"
eval "${SPARK_CMD}"