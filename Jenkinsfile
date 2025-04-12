pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/pasilva1/automacao_pyautogui_100425.git'
            }
        }

        stage('Deploy to Windows') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'windows-credentials', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    powershell '''
                        $securePassword = ConvertTo-SecureString $env:PASSWORD -AsPlainText -Force
                        $cred = New-Object System.Management.Automation.PSCredential ($env:USERNAME, $securePassword)

                        $session = New-PSSession -ComputerName 192.1.168.7 -Credential $cred

                        Invoke-Command -Session $session -ScriptBlock {
                            New-Item -ItemType Directory -Path 'C:\\app' -Force
                        }

                        Copy-Item -Path 'main.py' -Destination 'C:\\app\\main.py' -ToSession $session
                        Copy-Item -Path 'requirements.txt' -Destination 'C:\\app\\requirements.txt' -ToSession $session

                        Invoke-Command -Session $session -ScriptBlock {
                            python -m pip install --upgrade pip
                            pip install -r 'C:\\app\\requirements.txt'
                            Start-Process python -ArgumentList 'C:\\app\\main.py' -NoNewWindow
                        }

                        Remove-PSSession -Session $session
                    '''
                }
            }
        }
    }
}
