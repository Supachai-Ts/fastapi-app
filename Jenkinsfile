pipeline {
    agent {
        docker {
            image 'python:3.13'
            args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Supachai-Ts/fastapi-app.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
                sh 'pip install coverage pytest'
            }
        }
        stage('Run Tests & Coverage') {
            steps {
                sh 'pytest --cov=app tests/'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                sh '''
                  sonar-scanner \
                    -Dsonar.projectKey=fast-api \
                    -Dsonar.projectName=fast-api \
                    -Dsonar.host.url=http://localhost:9000 \
                    -Dsonar.login=sqp_c41ae5588b3862537947f865aab10481df349868
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fastapi-app:latest .'
            }
        }
        stage('Deploy Container') {
            steps {
                sh '''
                  docker stop fastapi-app || true
                  docker rm fastapi-app || true
                  docker run -d -p 8000:8000 --name fastapi-app fastapi-app:latest
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finished"
        }
    }
}
