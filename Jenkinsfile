pipeline {
	agent none
	stages {
		stage('Build') {
			environment {
				LAMBDA_FOLDER = "sample/Aws/Lambda"
			}
			agent { label 'slave01' }
			steps {
				sh 'python3.9 setup.py bdist_egg'
				sh 'zip -j ${LAMBDA_FOLDER}/Function ${LAMBDA_FOLDER}/PutMetadataToDb.py'
			}
		}
		stage('Deploy') {
			agent { label 'slave01' }
			environment {
				SCRIPT_FOLDER = "sample/Aws/emr"
				BUCKET_NAME = "s3://project.tweet.functions"
				RESOURCES_KEY = "${BUCKET_NAME}/resources/"
				SCRIPTS_KEY = "${BUCKET_NAME}/scripts/"
			}
			steps {				
				sh 'aws s3 cp ${SCRIPT_FOLDER}/Analysis/analysis.py ${SCRIPTS_KEY}'
				sh 'aws s3 cp ${SCRIPT_FOLDER}/Extraction/extraction.py ${SCRIPTS_KEY}'
				sh 'aws s3 cp ${SCRIPT_FOLDER}/Loading/loading.py ${SCRIPTS_KEY}'
				sh 'aws s3 cp ${SCRIPT_FOLDER}/Projection/projection.py ${SCRIPTS_KEY}'

				sh 'aws s3 cp scripts/Aws/bootstrap_action.sh ${RESOURCES_KEY}'
				sh 'aws s3 cp dist/Anomaly-0.1-py3.9.egg ${RESOURCES_KEY}'
				sh 'aws s3 cp dist/postgresql-42.2.8.jar ${RESOURCES_KEY}'
				sh 'aws s3 cp configs/emr/python_config.json ${RESOURCES_KEY}'

				sh 'aws s3 cp sample/Aws/Lambda/Function.zip ${RESOURCES_KEY}'
			}
		}
	}
}
