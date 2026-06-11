pipeline {

    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['TEST', 'DEV', 'PROD', 'XINING'],
            description: '测试环境选择'
        )
        booleanParam(
            name: 'SEND_EMAIL',
            defaultValue: false,
            description: '是否发送邮件通知'
        )
        booleanParam(
            name: 'SEND_WECHAT',
            defaultValue: true,
            description: '是否发送企业微信通知'
        )
    }

    environment {
        TEST_ENV    = "${params.ENVIRONMENT}"
        SEND_EMAIL  = "${params.SEND_EMAIL}"
        SEND_WECHAT = "${params.SEND_WECHAT}"
    }

    stages {
        // ==================== 1. 拉取代码 ====================
        stage('Checkout') {
            steps {
                container('python') {
                    checkout scm
                }
            }
        }
        // ==================== 2. 执行测试 ====================
        stage('Run Tests') {
            steps {
                container('python') {
                    sh '''
                        echo "========================================="
                        echo "  环境:         ${TEST_ENV}"
                        echo "  发送邮件:     ${SEND_EMAIL}"
                        echo "  发送企业微信: ${SEND_WECHAT}"
                        echo "========================================="
                        python3 --version || python --version
                        allure --version || echo "allure not found"
                        python3 run.py \
                            -env "${TEST_ENV}" \
                            --send-wechat "${SEND_WECHAT}" \
                            --send-email "${SEND_EMAIL}"
                    '''
                }
            }
        }

        // ==================== 3. 发布报告 ====================
        stage('Publish Reports') {
            parallel {
                // Allure 报告（需安装 Allure Jenkins Plugin）
                stage('Allure') {
                    steps {
                        allure includeProperties: false,
                            results: [[path: 'output/allure_result']]
                    }
                }
            }
        }

     // ==================== 4. 归档产物 ====================
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'output/**/*', allowEmptyArchive: true
            }
        }
    }

    // ==================== 后置清理 ====================
    post {
        always {
            cleanWs()
        }
        success {
            echo '测试执行成功'
        }
        failure {
            echo '测试执行失败，请检查 Allure 报告查看失败用例详情'
        }
    }
}
