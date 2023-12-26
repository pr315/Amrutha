pipeline {
    agent any
    environment {
        // Define environment variables
        DOCKER_IMAGE = 'prajval'  // Change this to your preferred image name
        TAG = 'latest'  // Change this as needed
        CONTAINER_PORT = 5000  // The port your container will listen on
        HOST_PORT = 5000  // The port on the host that will be mapped to the container port
    }
    stages {
    
        stage('Build') {
            steps {
                // Build your project (if necessary)
                echo 'Building...'
                // Add commands to build your project if needed
            }
        }
        stage('Test') {
            steps {
                // Run your tests
                echo 'Testing...'
                // Add commands to test your project
            }
        }
        stage('Dockerize') {
            steps {
                script {
                    // Build Docker image
                    sh '''
                    sudo apt update
                    sudo apt install lsof
                    lsof -v
                    sudo lsof -i -P -n | grep LISTEN
                    // docker --version
                    // docker build -t prajval:latest .
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // Run your container
                    sh '''
                    docker run -p 8080:8080 prajval:latest
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
