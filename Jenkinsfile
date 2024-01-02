pipeline {
    agent any

    stages {

        stage('Docker Status') {
            steps {
                script {
                    // Build Docker image
                    sh '''
                    chmod 777 ./scripts/docker.sh
                    ./scripts/docker.sh
                    '''
                }
            }
        }
    
        stage('Build the Web application') {
            steps {
                script {
                    // Build Docker image
                    sh '''
                    /usr/bin/docker build -t prajval:v3 .
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // Run your container
                    sh '''
                    /usr/bin/docker run -d -p 80:5000 prajval:v3
                    '''
                }
            }
        }
    }
    post {
        always {
            // Clean up, actions to perform after the pipeline runs
            sh '''
            exit 0
            '''
        }
    }
}
