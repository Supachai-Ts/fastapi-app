pipeline {
  agent {
    docker {
        image 'python-java:latest'
        args '-v /var/run/docker.sock:/var/run/docker.sock --user root'
    }
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'feature/test', url: 'https://github.com/Supachai-Ts/fastapi-app.git'
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
        sh '''
        . venv/bin/activate
        pytest --cov=app --cov-report=xml:coverage.xml --cov-report=term-missing tests/
        '''
        junit allowEmptyResults: true, testResults: 'tests/**/junit*.xml'
        archiveArtifacts artifacts: 'coverage.xml', onlyIfSuccessful: true
      }
    }

    stage('SonarQube Analysis') {
      steps {
        script {
          def scannerHome = tool name: 'SonarScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
          withSonarQubeEnv('SonarQube') {
            withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
              sh """
                ${scannerHome}/bin/sonar-scanner \
                  -Dsonar.projectKey=fast-api \
                  -Dsonar.projectName=fast-api \
                  -Dsonar.sources=./app \
                  -Dsonar.token=$SONAR_TOKEN
              """
            }
          }
        }
      }
    }
    stage('Quality Gate') {
      steps {
        timeout(time: 10, unit: 'MINUTES') {
          // ถ้าไม่ผ่าน Gate → pipeline fail
          waitForQualityGate abortPipeline: true
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
          docker run -d --restart=always \
          -e APP_ENV=staging \
          -p 9100:8000 \
          --name fastapi-app \
          fastapi-app:latest
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

