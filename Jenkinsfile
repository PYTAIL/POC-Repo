pipeline { 
    agent { label 'master' }
    environment {
        KUBECONFIG = credentials('a700aafc-b29c-4052-a8f8-c93863709f25')
        PATH = "PATH:/usr/local/bin"
    }    
    stages {
        stage('Setup') { 
            steps { 
                sh '''#!/bin/bash -ex
                    # Remove me after testing
                    python3 -m venv scenario
                    source scenario/bin/activate
                    pip install --exists-action i yamllint
                    pip install --exists-action i flake8
                    pip install --exists-action i pytest
                    pip install .
                    oc version
                '''
            }
        }
        stage('Flake8') { 
            steps { 
                sh '''#!/bin/bash -ex
                    source scenario/bin/activate
                    find . -name *.py | grep -v 'doc' | xargs -i flake8 {}  --show-source --max-line-length=120
                '''
            }
        }         
        stage('Pytest') { 
            steps { 
                sh '''#!/bin/bash -ex
                    source scenario/bin/activate
                    # export PATH=$PATH:/usr/local/bin/kubectl
                    ls -l /usr/local/bin
                    pytest -sv poc_repo/tests/resources/test_ocp_nodes.py
                '''
            }
        }
        stage('Cleanup') {
            steps {
                sh '''#!/bin/bash -ex
                    rm -rf scenario
                '''
            }
        }
    }
}
