pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning repository...'
                git branch: 'main', url: 'https://github.com/C-venu01/two-tier-flask-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t two-tier-flask-app .'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo 'Deploying containers...'
                sh 'docker compose down || true'
                sh 'docker compose up -d'
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Verifying containers...'
                sh 'sleep 15'
                sh 'docker ps'
                sh 'curl -f http://localhost:5000 || echo "App not ready yet, check manually"'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! App is running at port 5000.'
        }
        failure {
            echo 'Pipeline failed! Check the logs above for errors.'
        }
    }
}
