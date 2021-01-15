pipeline {
    agent none
    stages {
    	stage('Setup') {
	    agent { docker { image 'python:3.9.0'}
            }
            steps {
		sh 'python setup.py bdist_egg'
            }
        }
    }
}
