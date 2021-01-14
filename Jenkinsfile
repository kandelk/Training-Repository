pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
		echo 'Entering ...'
                git 'https://github.com/kandelk/Training-Repository.git'
		echo 'Finished'
            }
        }
	stage('Setup') {
            steps {
		bat "python setup.py bdist_egg"
            }
        }
    }
}
