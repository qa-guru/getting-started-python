pipeline {
    // Агенты jenkins.qa.guru с label 'python' — Linux-контейнеры с Python 3.14.
    // Selenium — чистый Python-пакет, ставится на musl (в отличие от Playwright).
    agent { label 'python-python314-jenkins-agent-1' }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timeout(time: 20, unit: 'MINUTES')
    }

    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Browser')
        string(name: 'BASE_URL', defaultValue: 'https://niffler.qa.guru', description: 'Base URL of the app under test')
        string(name: 'AUTH_URL', defaultValue: 'https://auth.niffler.qa.guru', description: 'Auth service URL')
        credentials(name: 'SELENOID_CREDENTIALS_ID', credentialType: 'Username with password', required: true, description: 'Credential с логином/токеном для selenoid.qa.guru (user-scope тоже виден в списке)')
    }

    environment {
        HEADLESS = 'true'
        BASE_URL = "${params.BASE_URL}"
        AUTH_URL = "${params.AUTH_URL}"
        SELENIUM_REMOTE = 'true'
        VENV = "${WORKSPACE}/.venv"
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                // catchError: падение тестов -> билд UNSTABLE, но pipeline продолжается
                // и Allure-отчёт генерируется в post-секции.
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    // Креды подставляются в URL только внутри шага и маскируются в логах
                    withCredentials([usernamePassword(
                        credentialsId: "${params.SELENOID_CREDENTIALS_ID}",
                        usernameVariable: 'SELENOID_USER',
                        passwordVariable: 'SELENOID_PASS'
                    )]) {
                        sh '''
                            . .venv/bin/activate
                            export SELENIUM_REMOTE_URL="https://${SELENOID_USER}:${SELENOID_PASS}@selenoid.qa.guru/wd/hub"
                            pytest --browser=${BROWSER} --alluredir=allure-results
                        '''
                    }
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
            // Секреты — два Secret text в Jenkins Credentials. Если они не
            // заведены, withCredentials бросит исключение — ловим и пропускаем.
            script {
                try {
                    withCredentials([
                        string(credentialsId: 'TELEGRAM_TOKEN', variable: 'TELEGRAM_TOKEN'),
                        string(credentialsId: 'TELEGRAM_CHAT_ID', variable: 'TELEGRAM_CHAT_ID')
                    ]) {
                        withEnv([
                            "REPO=${env.JOB_NAME}",
                            "BRANCH=${env.GIT_BRANCH ?: 'master'}",
                            "COMMIT=${env.GIT_COMMIT ?: ''}",
                            "RUN_URL=${env.BUILD_URL}",
                            "REPORT_URL=${env.BUILD_URL}allure"
                        ]) {
                            sh '''
                                TRIGGER="jenkins build #${BUILD_NUMBER}"
                                export TRIGGER
                                . .venv/bin/activate 2>/dev/null || true
                                python3 notify_telegram.py
                            '''
                        }
                    }
                } catch (Exception e) {
                    echo "Telegram notification skipped: ${e.message}"
                }
            }
        }
        unsuccessful {
            archiveArtifacts artifacts: 'artifacts/**', allowEmptyArchive: true
        }
        cleanup {
            cleanWs()
        }
    }
}
