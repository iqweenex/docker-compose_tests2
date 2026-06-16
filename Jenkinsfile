pipeline {
    agent any

    environment {
        // GitHub credentials для доступа к репозиторию
        GITHUB_CREDS = credentials('github-credentials')

        // PostgreSQL credentials из Jenkins
        POSTGRES_CREDS = credentials('postgres-credentials')

        // Распаковываем логин и пароль из credentials
        POSTGRES_USER = "${POSTGRES_CREDS_USR}"
        POSTGRES_PASSWORD = "${POSTGRES_CREDS_PSW}"

        // Настройки БД
        POSTGRES_DB_AUTH = 'auth_db'
        POSTGRES_DB_UNIVERSITY = 'university_db'

        // URL для сервисов (внутри Docker сети)
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

        stage('Setup Python') {
            steps {
                sh '''
                    python3 --version
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
                    EOF
                    echo "=== .env file created successfully ==="
                '''
            }
        }

        stage('Start Services') {
            steps {
                sh '''
                    # Останавливаем старые контейнеры
                    docker-compose down -v || true

                    # Запускаем сервисы
                    docker-compose up -d

                    # Ждем готовности сервисов
                    echo "Waiting for services to be ready..."

                    # Ждем auth сервис (порт 8000)
                    timeout 120 bash -c 'while ! curl -s http://localhost:8000/docs > /dev/null; do echo "Waiting for auth..."; sleep 3; done'

                    # Ждем university сервис (порт 8001)
                    timeout 120 bash -c 'while ! curl -s http://localhost:8001/docs > /dev/null; do echo "Waiting for university..."; sleep 3; done'

                    echo "=== All services are ready ==="
                    docker-compose ps
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -v --alluredir=allure-results
                '''
            }
            post {
                always {
                    // Сохраняем результаты тестов в JUnit формате
                    junit '**/report.xml' || true

                    // Сохраняем логи
                    archiveArtifacts artifacts: '**/*.log', fingerprint: true || true

                    // Сохраняем Allure результаты
                    archiveArtifacts artifacts: 'allure-results/**', fingerprint: true || true
                }
            }
        }
    }

    post {
        always {
            // Останавливаем контейнеры после тестов
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