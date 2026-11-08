pipeline {
    // Агенты jenkins.qa.guru с label 'python' — Linux-контейнеры с Python 3.14.
    agent { label 'python' }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timeout(time: 20, unit: 'MINUTES')
    }

    parameters {
        choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Browser engine')
        string(name: 'BASE_URL', defaultValue: 'https://niffler.qa.guru', description: 'Base URL of the app under test')
        string(name: 'AUTH_URL', defaultValue: 'https://auth.niffler.qa.guru', description: 'Auth service URL')
    }

    environment {
        HEADLESS = 'true'
        BASE_URL = "${params.BASE_URL}"
        AUTH_URL = "${params.AUTH_URL}"
        VENV = "${WORKSPACE}/.venv"
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 --version
                    pip config list || true
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt || \
                        pip install -r requirements.txt -i https://pypi.org/simple
                '''
            }
        }

        stage('Browsers') {
            steps {
                sh '''
                    . .venv/bin/activate
                    playwright install ${BROWSER} --with-deps || playwright install ${BROWSER}
                '''
            }
        }

        stage('Test') {
            steps {
                // catchError: падение тестов -> билд UNSTABLE, но pipeline продолжается
                // и Allure-отчёт генерируется в post-секции.
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        . .venv/bin/activate
                        pytest --browser=${BROWSER} --alluredir=allure-results
                    '''
                }
            }
        }
    }

    post {
        always {
            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
        }
        unsuccessful {
            archiveArtifacts artifacts: 'artifacts/**', allowEmptyArchive: true
        }
        cleanup {
            cleanWs()
        }
    }
}
