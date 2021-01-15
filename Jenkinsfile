pipeline {
    agent { docker { image 'python:3.9.0' } }

    stages {
    	stage('Setup') {
            steps {
		sh 'python --version'
            }
        }
    }
}
