pipeline {
    // Агент публикует Allure; Python и браузеры запускаются в glibc-контейнере.
    // Нужны Docker CLI, доступ к Docker daemon (плагин Docker Pipeline не требуется).
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
    }

    stages {
        stage('Docker availability') {
            steps {
                sh '''
                    if ! command -v docker >/dev/null 2>&1; then
                        echo 'Docker CLI is required on the Jenkins agent to run Playwright.' >&2
                        exit 1
                    fi
                    if ! docker info >/dev/null 2>&1; then
                        echo 'The Jenkins agent needs access to a running Docker daemon.' >&2
                        exit 1
                    fi
                '''
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    sh ci/run-playwright.sh sh -ec '
                        python3 --version
                        python3 -m venv .venv
                        .venv/bin/python -m pip install -r requirements.txt
                    '
                '''
            }
        }

        stage('Test') {
            steps {
                // Браузеры и системные зависимости уже включены в образ.
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        sh ci/run-playwright.sh .venv/bin/python -m pytest --browser="${BROWSER}" --alluredir=allure-results
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
