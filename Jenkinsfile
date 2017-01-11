node {

    properties([
        buildDiscarder(
            logRotator(artifactDaysToKeepStr: '1', artifactNumToKeepStr: '2', daysToKeepStr: '', numToKeepStr: '3')
        ),
        parameters([
            string(name: 'branch_to_build', defaultValue: 'include_assert_tests'                   , description: 'Branch name to work on'),
            string(name: 'client_id'      , defaultValue: ''                                       , description: 'Client ID'),
            string(name: 'client_secret'  , defaultValue: ''                                       , description: 'Client Secret'),
            string(name: 'orcid_id'       , defaultValue: '0000-0003-4962-7157'                    , description: 'Latest orcid id'),
            string(name: 'search_value'   , defaultValue: '10032016'                               , description: 'Username suffix to search')
        ]),        
        [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false],
        pipelineTriggers([])
    ])
    
    git url: 'https://github.com/ORCID/orcid-independent-tests.git', branch: params.branch_to_build
    
    stage('Crate properties file'){
        writeFile file: 'test-client.properties', text: "clientId=$client_id\nclientSecret=$client_secret\nsearchValue=$search_value\norcidId=$orcid_id\n"
    }
    
    stage('Prepare Environment'){
        sh "rm -rf .py_env results"
        sh "virtualenv .py_env"
        sh "mkdir results"
    }
    
    stage('Run Test'){
        try {
            sh ". .py_env/bin/activate && pip2 install -r ./requirements.txt && py.test --junitxml results/test_public_api_read_search.xml test_public_api_read_search.py"
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        } finally {
            junit 'results/*.xml'
        }
    }
}