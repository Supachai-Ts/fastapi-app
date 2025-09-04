pipeline {
  agent {
    docker {
        image 'python-java:latest'
        args '-v /var/run/docker.sock:/var/run/docker.sock'
    }
}

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/Supachai-Ts/fastapi-app.git'
      }
    }

    stage('Install Java for SonarQube') {
        steps {
            sh '''
                apt-get update && apt-get install -y openjdk-17-jre
                java -version
            '''
        }
    }

    stage('Install Dependencies') {
        steps {
            sh '''
                python -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install coverage pytest pytest-cov
            '''
        }       
    }


    stage('Run Tests & Coverage') {
      steps {
        sh 'pytest --cov=app tests/'
      }
    }

    stage('SonarQube Analysis') {
      steps {
        script {
          // ใช้ SonarScanner จาก Global Tool
          def scannerHome = tool name: 'SonarScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
          withSonarQubeEnv('SonarQube') {
            sh """
              ${scannerHome}/bin/sonar-scanner \
                -Dsonar.projectKey=fast-api \
                -Dsonar.projectName=fast-api \
                -Dsonar.sources=./app
            """
          }
        }
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
