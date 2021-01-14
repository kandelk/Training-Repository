pipeline {
    agent any

    stages {
    	stage('Setup') {
            steps {
		sh "python setup.py bdist_egg"
            }
        }
    }
}
