pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                git 'https://github.com/kandelk/Training-Repository.git'

                sh "python setup.py bdist_egg"

                // bat "mvn -Dmaven.test.failure.ignore=true clean package"
				// bat "python setup.py bdist_egg"
            }
        }
    }
}
