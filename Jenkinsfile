pipeline {
    // Агенты jenkins.qa.guru с label 'python' — Linux-контейнеры с Python 3.14.
    agent { label 'python-python314-jenkins-agent-1' }

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
                    uname -a
                    python3 --version
                    python3 -c "import platform; print(platform.platform()); print('libc:', platform.libc_ver()); print('arch:', platform.machine())"
                    ldd --version 2>&1 | head -1 || true
                    pip config list || true
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip debug --verbose 2>/dev/null | grep -A2 "Compatible tags" | head -8 || true
                    pip install -r requirements.txt
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
