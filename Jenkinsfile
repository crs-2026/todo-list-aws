pipeline {
    agent any

    environment {
        // ========== CONFIGURACIÓN DE PRODUCCIÓN ==========
        AWS_DEFAULT_REGION = 'us-east-1' 
        STACK_NAME         = 'todo-list-aws-production' // Nombre del Stack diferenciado para Producción
        S3_BUCKET          = 'aws-sam-cli-managed-default-samclisourcebucket-w2rxf671dndk' // Mi bucket de artefactos SAM
        GIT_REPO_URL       = 'https://github.com/crs-2026/todo-list-aws.git'
    }

    stages {
        /*
         * =====================================================
         * 1. GET CODE (Rama Master)
         * =====================================================
         */
        stage('Get Code') {
            steps {
                echo 'Descargando el código fuente consolidado desde la rama master...'
                git branch: 'master', url: "${env.GIT_REPO_URL}"
            }
        }

        /*
         * =====================================================
         * 2. DEPLOY (Production Environment)
         * =====================================================
         */
        stage('Deploy') {
            steps {
                echo 'Desplegando la aplicación en el entorno de producción...'
                sh '''
                sam build
                
                # Desplegamos pasando explícitamente el parámetro de Stage como "production"
                sam deploy \
                    --stack-name ${STACK_NAME} \
                    --s3-bucket ${S3_BUCKET} \
                    --capabilities CAPABILITY_IAM \
                    --no-confirm-changeset \
                    --no-fail-on-empty-changeset \
                    --parameter-overrides Stage="production"
                '''
            }
        }

        /*
         * =====================================================
         * 3. REST TEST (Solo Lectura)
         * =====================================================
         */
        stage('Rest Test') {
            steps {
                echo 'Identificando la URL de producción y ejecutando pruebas de solo lectura...'
                sh '''
                # Extraemos el endpoint generado dinámicamente para el stack de producción
                export API_URL=$(aws cloudformation describe-stacks \
                    --stack-name ${STACK_NAME} \
                    --query "Stacks[0].Outputs[?OutputKey=='BaseUrlApi'].OutputValue" \
                    --output text)
                
                echo "Endpoint de Producción Detectado: $API_URL"
                
                # Configuración del entorno aislado de pruebas
                python3 -m venv venv_production_tests
                . venv_production_tests/bin/activate
                pip install --upgrade pip
                pip install pytest requests
                
                # Inyectamos el endpoint de producción
                export BASE_URL=$API_URL
                
                # Ejecutamos exclusivamente el test de listado (Lectura) 
                # Evitamos lanzar POST, PUT o DELETE que alteren la base de datos de producción.
                pytest -k "listtodos" --junitxml=result-production.xml test/integration/todoApiTest.py
                
                deactivate
                '''
            }
            post {
                always {
                    // Publicamos el resultado en el panel de Jenkins
                    junit testResults: 'result-production.xml', allowEmptyResults: true
                }
            }
        }
    }

    post {
        always {
            echo 'Limpiando el espacio de trabajo del agente de CD...'
            cleanWs()
        }
    }
}