pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                git 'https://github.com/kandelk/Training-Repository.git'
            }
        }
	stage('Setup') {
            steps {
		bat "python setup.py bdist_egg"
            }
        }
    }
}
