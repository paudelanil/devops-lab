pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = "docker-compose.yml"
    }

    stages {
        stage('Clone Source Code') {
            steps {
                // Clone the source code from the configured repository
                git url: 'https://github.com/your-repo/your-project.git', branch: 'main'
            }
        }

        stage('Build Containers') {
            steps {
                script {
                    // Ensure Docker Compose is using the correct context and build all services
                    sh "docker-compose -f ${DOCKER_COMPOSE_FILE} build"
                }
            }
        }

        stage('Run Containers') {
            steps {
                script {
                    // Stop and remove any existing containers to avoid conflicts
                    sh "docker-compose -f ${DOCKER_COMPOSE_FILE} down || true"

                    // Start the containers
                    sh "docker-compose -f ${DOCKER_COMPOSE_FILE} up -d"
                }
            }
        }

        stage('Verify Services') {
            steps {
                script {
                    // Check if containers are running
                    sh "docker ps"
                }
            }
        }
    }

    post {
        always {
            // Clean up any running containers if necessary
            script {
                echo "Checking running containers..."
                agrish "docker-compose -f ${DOCKER_COMPOSE_FILE} ps"
            }
        }
    }
}

