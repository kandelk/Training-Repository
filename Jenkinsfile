pipeline {
	agent none
	stages {
		stage('Build') {
			agent { docker { image 'python:3.9.0'} }
			steps {
				sh 'python setup.py bdist_egg'
			}
		}
		stage('Deploy') {
			agent { docker { image 'python:3.9.0'} }
			environment {
				SCRIPT_FOLDER = "sample/Aws/emr"
				BUCKET_NAME = "s3://project.tweet.functions"
			}
			steps {
				sh 'aws s3 cp dist/Anomaly-0.1-py3.9.egg ${BUCKET_NAME}'
				sh 'aws s3 cp ${SCRIPT_FOLDER}/Analysis/analysis.py ${BUCKET_NAME}/scripts'
			}
		}
	}
}
