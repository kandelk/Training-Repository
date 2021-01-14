pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                git 'https://github.com/kandelk/Training-Repository.git'

                //sh "python setup.py bdist_egg"
		//bat "python setup.py bdist_egg"
            }
        }
	stage('Setup') {
            steps {
		bat "python setup.py bdist_egg"
            }
        }
    }
}
