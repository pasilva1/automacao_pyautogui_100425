pipeline {
    agent any

    environment {
        REMOTE_HOST = '192.168.1.7'
        REMOTE_PATH = 'C:/app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/pasilva1/automacao_pyautogui_100425.git'
            }
        }

        stage('Deploy via SSH') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'windows-credentials', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                        echo "📁 Criando diretório no remoto..."
                        sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USERNAME@$REMOTE_HOST" "powershell -Command \\"New-Item -Path '$REMOTE_PATH' -ItemType Directory -Force\\""

                        echo "📤 Enviando arquivos..."
                        sshpass -p "$PASSWORD" scp -o StrictHostKeyChecking=no main.py requirements.txt "$USERNAME@$REMOTE_HOST:$REMOTE_PATH/"

                        echo "🚀 Executando main.py..."
                        sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USERNAME@$REMOTE_HOST" "powershell -Command \\"cd '$REMOTE_PATH'; pip install -r requirements.txt; python main.py\\""
                    '''
                }
            }
        }
    }
}
