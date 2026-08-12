pipeline {

    agent any

    environment {
        IMAGE_NAME = "kind-devops-backend"
        IMAGE_TAG = "v${BUILD_NUMBER}"
        NAMESPACE = "devops-demo"
        KIND_CLUSTER = "devops-lab"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${IMAGE_TAG} \
                      ./app
                '''
            }
        }

        stage('Load Image into Kind') {
            steps {
                sh '''
                    kind load docker-image \
                      ${IMAGE_NAME}:${IMAGE_TAG} \
                      --name ${KIND_CLUSTER}
                '''
            }
        }

        stage('Deploy PostgreSQL') {
            steps {
                sh '''
                    kubectl apply \
                      -f k8s/postgres.yaml
                '''
            }
        }

        stage('Wait for PostgreSQL') {
            steps {
                sh '''
                    kubectl rollout status \
                      deployment/postgres \
                      -n ${NAMESPACE} \
                      --timeout=120s
                '''
            }
        }

        stage('Deploy Backend') {
            steps {
                sh '''
                    sed "s|kind-devops-backend:v1|${IMAGE_NAME}:${IMAGE_TAG}|g" \
                      k8s/backend.yaml \
                      | kubectl apply -f -
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl rollout status \
                      deployment/backend \
                      -n ${NAMESPACE} \
                      --timeout=120s
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    kubectl run ci-smoke-test \
                      --rm \
                      -i \
                      --restart=Never \
                      --image=curlimages/curl:8.10.1 \
                      -n ${NAMESPACE} \
                      -- curl \
                      --fail \
                      --max-time 10 \
                      http://backend:5000/health
                '''
            }
        }
    }

    post {

        success {
            echo 'Deployment successful!'
        }

        failure {
            echo 'Deployment failed. Check Kubernetes and Jenkins logs.'
        }
    }
}
