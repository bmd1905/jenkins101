pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }

    environment {
        registry = 'bmd1905/jenkins101_gitlab'
        registryCredential = 'dockerhub'
        containerName = 'my-app-container'
        dockerImage = ''
    }

    stages {
        stage('Test') {
            agent {
                docker {
                    image 'python:3.8'
                    args '-v $WORKSPACE:/app -w /app'
                }
            }
            steps {
                echo 'Testing model correctness..'
                sh 'pip install -r requirements.txt'
                sh 'pytest'
            }
        }
        stage('Build') {
            steps {
                script {
                    echo 'Building Docker image for deployment..'
                    dockerImage = docker.build("${registry}:${BUILD_NUMBER}")
                    echo 'Pushing Docker image to DockerHub..'
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying models..'
                script {
                    try {
                        sh "docker stop ${containerName} || true"
                        sh "docker rm ${containerName} || true"
                        sh "docker pull ${registry}:latest"
                        sh """
                            docker run -d --name ${containerName} \\
                            -p 8080:8080 -p 30000:30000 \\
                            ${registry}:latest
                        """
                        echo 'Deployment completed'
                    } catch (Exception e) {
                        echo 'Deployment failed: ${e.getMessage()}'
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }
    }
    post {
        always {
            echo 'Cleaning up...'
            // Add any necessary cleanup tasks
        }
        success {
            echo 'Build succeeded!'
        }
        failure {
            echo 'Build failed.'
        }
        unstable {
            echo 'Build is unstable.'
        }
    }
}
