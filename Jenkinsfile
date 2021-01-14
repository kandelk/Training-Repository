pipeline {
    agent { docker { image 'python:3.7.2' } }

    stages {
    	stage('Setup') {
            steps {
		bat 'python --version'
            }
        }
    }
}
