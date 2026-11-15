pipeline {
    agent any

    environment {
        UV_SYSTEM_PYTHON = '1'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment & Dependencies') {
            steps {
                sh '''
                    # Ensure uv is available in path or install it if missing
                    if ! command -v uv &> /dev/null; then
                        echo "uv not found, installing standalone uv..."
                        curl -LsSf https://astral.sh/uv/install.sh | sh
                        export PATH="$HOME/.local/bin:$PATH"
                    fi
                    uv --version
                    uv sync
                '''
            }
        }

        stage('Run Unit & API Tests') {
            steps {
                sh '''
                    mkdir -p reports
                    uv run pytest --junitxml=reports/junit-results.xml -v
                '''
            }
        }

        stage('Generate Evidently Monitoring Reports') {
            steps {
                sh '''
                    uv run python -m arithmetic_service.monitoring
                '''
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/junit-results.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline completed successfully with all tests and Evidently reports!'
        }
        failure {
            echo 'Pipeline failed during test execution or Evidently report generation.'
        }
    }
}
