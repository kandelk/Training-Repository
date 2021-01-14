pipeline {
    agent any

    stages {
    	stage('Setup') {
            steps {
		bat 'echo "Entering ..."'
		bat "python setup.py bdist_egg"
            }
        }
    }
}
