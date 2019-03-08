def pytest(unit){
    try {
        sh ". .py_env/bin/activate && py.test -v -r fxE --junitxml results/${unit}.xml orcid/${unit}.py"
    } catch(Exception err) {
        def err_msg = err.getMessage()
        echo "PYTEST PROBLEM: $err_msg"
        throw err
    } finally {
        junit 'results/*.xml'
        sh 'rm -rf results/*.xml'
    }
}

node {

    properties([
        buildDiscarder(
            logRotator(artifactDaysToKeepStr: '5', artifactNumToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
        ),
        parameters([
            string(name: 'branch_to_build'       , defaultValue: 'master'                                         , description: 'Branch name to work on'),
            string(name: 'test_server'           , defaultValue: 'qa.orcid.org'                                   , description: 'Base domain name to test'),            
            string(name: 'client_secrets_file'   , defaultValue: '/var/lib/jenkins/orcidclients.py'               , description: 'Properties file with predefined secrets')
        ]),
        [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false]
    ])

    git url: 'https://github.com/ORCID/orcid-independent-tests.git', branch: params.branch_to_build

    stage('configure'){
        sh "rm -f orcid/properties.py"
        writeFile file: 'testinputs.py', text: "test_server=\"$test_server\""
        sh "cat $client_secrets_file testinputs.py > orcid/properties.py"
        sh "rm -rf .py_env results *.secret ${WORKSPACE}/xvfb && mkdir results ${WORKSPACE}/xvfb"
        sh "virtualenv .py_env"
        sh ". .py_env/bin/activate && pip2 install -q -r orcid/requirements.txt"
    }

    stage('TEST LIMITED RECORD'){
        try {
            pytest 'test_limited_record'
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }

    stage('TEST PRIVATE RECORD'){
        try {
            pytest 'test_private_record'
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }

    stage('TEST PUBLIC RECORD'){
        try {
            pytest 'test_public_record'
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }

    stage('TEST SCOPED METHODS'){
        try {
            pytest 'test_scope_methods'
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }

    stage ('finalize'){
        deleteDir()
    }

}

