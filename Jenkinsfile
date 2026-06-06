pipeline {
    agent any

    environment {
        // ========== CONFIGURACIÓN REQUERIDA ==========
        AWS_DEFAULT_REGION = 'us-east-1' 
        STACK_NAME         = 'todo-list-aws'
        S3_BUCKET          = 'aws-sam-cli-managed-default-samclisourcebucket-w2rxf671dndk' 
        GIT_REPO_URL       = 'https://github.com/crs-2026/todo-list-aws.git'
    }

    stages {
        /*
         * =====================================================
         * 1. GET CODE
         * =====================================================
         */
        stage('Get Code') {
            steps {
                echo 'Descargando el código fuente (rama develop)...'
                git branch: 'develop', url: "${env.GIT_REPO_URL}"
            }
        }

        /*
         * =====================================================
         * 2. STATIC TEST
         * =====================================================
         */
        stage('Static') {
            steps {
                echo 'Ejecutando análisis estático con Flake8...'
                sh '''
                export PYTHONPATH=$WORKSPACE
                # Analizamos la carpeta /src. 
                python3 -m flake8 --exit-zero src > flake8.out
                '''
                // Publicamos el informe 
                archiveArtifacts artifacts: 'flake8.out', fingerprint: true
            }
        }

        /*
         * =====================================================
         * 3. SECURITY
         * =====================================================
         */
        stage('Security Test') {
            steps {
                echo 'Ejecutando pruebas de seguridad con Bandit...'
                sh '''
                export PYTHONPATH="${WORKSPACE}"
                python3.12 -m venv venv
                . venv/bin/activate
                
                pip install --upgrade pip
                pip install bandit
                
                # Analiza la carpeta /src.
                bandit --exit-zero -r ./src -f custom -o bandit.out \
                    --msg-template "{abspath}:{line}: [{test_id}({severity})] {msg}"
                deactivate
                '''
                // Publicamos el informe de seguridad
                archiveArtifacts artifacts: 'bandit.out', fingerprint: true
            }
        }

        /*
         * =====================================================
         * 4. DEPLOY (AWS SAM)
         * =====================================================
         */
        stage('Deploy') {
            steps {
                echo 'Construyendo y desplegando en el entorno de Staging...'
                sh '''
                sam build
                
                # Pasamos el parametro --parameter-overrides para avisarle al template que estamos en staging
                sam deploy \
                    --stack-name ${STACK_NAME} \
                    --s3-bucket ${S3_BUCKET} \
                    --capabilities CAPABILITY_IAM \
                    --no-confirm-changeset \
                    --no-fail-on-empty-changeset \
                    --parameter-overrides Stage="staging"
                '''
            }
        }

        /*
         * =====================================================
         * 5. REST TEST (Pruebas Dinámicas con Pytest)
         * =====================================================
         */
       stage('Rest Test') {
            steps {
                echo 'Obteniendo Endpoint de la API y ejecutando pruebas dinámicas...'
                sh '''
                #Buscamos "BaseUrlApi"
                export API_URL=$(aws cloudformation describe-stacks \
                    --stack-name ${STACK_NAME} \
                    --query "Stacks[0].Outputs[?OutputKey=='BaseUrlApi'].OutputValue" \
                    --output text)
                
                echo "Endpoint detectado: $API_URL"
                
                python3 -m venv venv_tests
                . venv_tests/bin/activate
                pip install --upgrade pip
                pip install pytest requests
                
                export BASE_URL=$API_URL
                
                pytest --junitxml=result-integration.xml test/integration/todoApiTest.py
                deactivate
                '''
            }
            post {
                always {
                    // Muestra los resultados en el panel de Jenkins
                    // Si falla un test, la etapa se marcará en rojo automáticamente
                    junit testResults: 'result-integration.xml', allowEmptyResults: true
                }
            }
        }
     
        /*
         * =====================================================
         * 6. PROMOTE (Merge a Master)
         * =====================================================
         */
        stage('Promote') {
            steps {
                echo 'Promocionando código a producción (Merge de Develop -> master)...'
                
                
                withCredentials([usernamePassword(credentialsId: 'Jenkins', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                    sh '''
                    git config user.name "crs"
                   
                    
                    # Traemos la rama master limpia del servidor
                    git fetch origin master:master
                    git checkout master
                    
                    # Hacemos merge de los cambios aprobados
                    git merge origin/develop --no-edit
                    
                    # Inyectamos credenciales de manera segura para hacer push al repositorio remoto
                    git remote set-url origin https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/crs-2026/todo-list-aws.git
                    git push origin master
                    '''
                }
            }
        }
    
    }
        

    post {
        always {
            echo 'Limpiando el Workspace del Agente...'
            cleanWs()
        }
    }
  }
