pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock --network university-tests_default'
        }
    }

    environment {
        GITHUB_CREDS = credentials('github-credentials')
        POSTGRES_CREDS = credentials('postgres-credentials')
        POSTGRES_USER = "${POSTGRES_CREDS_USR}"
        POSTGRES_PASSWORD = "${POSTGRES_CREDS_PSW}"
        POSTGRES_DB_AUTH = 'auth_db'
        POSTGRES_DB_UNIVERSITY = 'university_db'
        AUTH_SERVICE_INTERNAL_URL = 'http://auth:8000'
        AUTH_SERVICE_API_URL = 'http://auth:8000'
        UNIVERSITY_SERVICE_INTERNAL_URL = 'http://university:8000'
        UNIVERSITY_SERVICE_API_URL = 'http://university:8000'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'develop',
                    url: 'https://github.com/iqweenex/docker-compose_tests2.git',
                    credentialsId: 'github-credentials'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    apt-get update
                    apt-get install -y python3-venv curl
                    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                    chmod +x /usr/local/bin/docker-compose
                    python3 --version
                    docker-compose --version
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Create .env file') {
            steps {
                sh '''
                    cat > .env << EOF
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB_AUTH=${POSTGRES_DB_AUTH}
POSTGRES_DB_UNIVERSITY=${POSTGRES_DB_UNIVERSITY}
AUTH_SERVICE_INTERNAL_URL=${AUTH_SERVICE_INTERNAL_URL}
AUTH_SERVICE_API_URL=${AUTH_SERVICE_API_URL}
UNIVERSITY_SERVICE_INTERNAL_URL=${UNIVERSITY_SERVICE_INTERNAL_URL}
UNIVERSITY_SERVICE_API_URL=${UNIVERSITY_SERVICE_API_URL}
AUTH_SERVICE_URL=${AUTH_SERVICE_INTERNAL_URL}
UNIVERSITY_SERVICE_URL=${UNIVERSITY_SERVICE_INTERNAL_URL}
EOF
                '''
                sh 'echo "=== .env file created successfully ==="'
                sh 'cat .env'
            }
        }

        stage('Start Services') {
            steps {
                sh '''
                    docker-compose down -v --remove-orphans || true
                    docker-compose up -d

                    echo "Waiting for services to be ready..."

                    timeout 120 bash -c 'while ! curl -s http://auth:8000/docs > /dev/null; do echo "Waiting for auth..."; sleep 3; done'
                    timeout 120 bash -c 'while ! curl -s http://university:8000/docs > /dev/null; do echo "Waiting for university..."; sleep 3; done'

                    echo "=== All services are ready ==="
                    docker-compose ps
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    export AUTH_SERVICE_URL=http://auth:8000
                    export UNIVERSITY_SERVICE_URL=http://university:8000
                    export AUTH_SERVICE_API_URL=http://auth:8000
                    export UNIVERSITY_SERVICE_API_URL=http://university:8000
                    pytest -v --alluredir=allure-results
                '''
            }
            post {
                always {
                    junit testResults: '**/report.xml', allowEmptyResults: true
                    archiveArtifacts artifacts: 'allure-results/**', fingerprint: true || true
                }
            }
        }
    }

    post {
        always {
            sh '''
                docker-compose down -v
            '''
        }
        success {
            echo '✅ Все тесты успешно пройдены!'
        }
        failure {
            echo '❌ Некоторые тесты не прошли! Проверьте логи.'
        }
    }
}