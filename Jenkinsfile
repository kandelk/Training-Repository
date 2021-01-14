pipeline {
    agent any

    stages {
    	stage('Setup') {
            steps {
		sh 'echo "Entering ..."'
		sh "python setup.py bdist_egg"
            }
        }
    }
}
