pipeline {
    agent any    
    environment {
        VENV_DIR = '/var/jenkins_home/workspace/Publicacion/venv'
    }
    stages {
        //stage('Clean Up and Checkout ') {
            //steps {
                //deleteDir()
                // Clonar el repositorio Git
                //git url: 'https://github.com/ericruizINE/descargaCSV.git', branch: 'main'
            //}
        //}
        stage('Install & Setup venv') {
            steps {
                // Instalar el paquete python3-venv si aún no está instalado
                sh 'apt-get update && apt-get install -y python3-venv'
                sh 'apt-get update && apt-get install -y python3-pip'
                sh "python3 -m venv ${VENV_DIR}"
            }
        }
        stage('Install Dependencies') {
            steps {
                // Activar el entorno virtual e instalar las dependencias
                sh """
                    . ${VENV_DIR}/bin/activate
                    pip install --no-cache-dir -r requirements.txt
                """
            }
        }
        stage('Descarga de Archivos CSV Presidencia') {
          steps {
            sh """
                    . ${VENV_DIR}/bin/activate > /dev/null 2>&1
                    python3 24-05-07-BD-Descarga-Descomprimir_1.py
                    python3 presidencia.py
                    python3 publicacion.py
               """
          }
        }
        stage('Mostrar Screenshot URLs') {
            steps {
                script {
                    // Mostrar las URLs de las capturas de pantalla
                    def screenshots = sh(script: "ls ${WORKSPACE}/screenshots_publi/*.png", returnStdout: true).trim().split('\n')
                    screenshots.each { screenshot ->
                        echo "Screenshot URL: ${env.BUILD_URL}execution/node/3/ws/screenshots_publi/${screenshot.split('/').last()}"
                                     }
                    }
                script {
                    // Mostrar las URLs de los archivos
                    def files = sh(script: "ls ${WORKSPACE}/Archivos/*.csv", returnStdout: true).trim().split('\n')
                    files.each { file ->
                        echo "Files URL: ${env.BUILD_URL}execution/node/3/ws/Archivos/${file.split('/').last()}"
                                     }
                    }
            }
        }
        stage('Ejecutar Pytest') {
            steps {
                sh """
                    . ${VENV_DIR}/bin/activate > /dev/null 2>&1
                    pytest presidencia.py --alluredir=report
                    pytest publicacion.py --alluredir=report
                    pytest pytestpubli.py --alluredir=report
               """
            }
        }
        stage('Publicar Reporte Allure') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'report']]
                    ])
                  }
        }
    }
    post {
        always {
            script {
                // Publica la URL del reporte en la consola de Jenkins
                def allureReportUrl = "${env.BUILD_URL}allure"
                echo "El reporte de Allure está disponible en: ${allureReportUrl}"
            }
        }
    }
}
