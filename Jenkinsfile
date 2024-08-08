pipeline {
    agent any

    options{
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }

    environment{
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
                }
            }
            steps {
                echo 'Testing model correctness..'
                sh 'pip install -r requirements.txt && pytest'
            }
        }
        stage('Build') {
            steps {
                script {
                    echo 'Building image for deployment..'
                    dockerImage = docker.build registry + ":$BUILD_NUMBER" 
                    echo 'Pushing image to dockerhub..'
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying models..'
                sh """
                    # Stop and remove the existing container if it exists
                    docker stop ${containerName} || true
                    docker rm ${containerName} || true

                    # Pull the latest image
                    docker pull ${registry}:latest

                    # Run the new container
                    docker run -d --name ${containerName} -p 8080:8080 ${registry}:latest
                """
                echo 'Deployment completed'
            }
        }
    }
}