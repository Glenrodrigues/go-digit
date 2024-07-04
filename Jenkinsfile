pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/Glenrodrigues/go-digit.git'
        DOCKER_IMAGE = 'godigitapp'
        ECR_REGISTRY = '600453958506.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO = 'go-digit-docker-private'
        AWS_REGION = 'us-east-1'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Glenrodrigues/go-digit.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${env.DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        stage('Login to ECR') {
            steps {
                sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 600453958506.dkr.ecr.us-east-1.amazonaws.com'
                sh 'docker tag godigitapp:latest 600453958506.dkr.ecr.us-east-1.amazonaws.com/go-digit-docker-private-app:latest'
                sh 'docker push 600453958506.dkr.ecr.us-east-1.amazonaws.com/go-digit-docker-private-app:latest'
            }
        }

        stage('Run Terraform') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                    dir('terraform') {
                        sh 'terraform init'
                        sh 'terraform apply -auto-approve'
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
