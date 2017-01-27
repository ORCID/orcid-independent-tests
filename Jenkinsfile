node {

    properties([
        buildDiscarder(
            logRotator(artifactDaysToKeepStr: '5', artifactNumToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
        ),
        parameters([
            string(name: 'branch_to_build'       , defaultValue: 'master'                                               , description: 'Branch name to work on'),
            string(name: 'read_code'             , defaultValue: 'abcdef'                                               , description: 'Six digits code with read privileges'),            
            string(name: 'orcid_id'              , defaultValue: '0000-0003-4962-7157'                                  , description: 'Latest orcid id'),
            string(name: 'search_value'          , defaultValue: '10Jan2017'                                            , description: 'Username suffix to search'),
            string(name: 'member_code'           , defaultValue: 'ghtlms'                                               , description: 'Six digits code with post/update privileges'),
            string(name: 'client_secrets_file'   , defaultValue: '/var/lib/jenkins/workspace/ORCID-independent-tests/'  , description: 'Properties file with predefined secrets')
        ]),        
        [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false]
    ])
    
    git url: 'https://github.com/ORCID/orcid-independent-tests.git', branch: params.branch_to_build
    
    stage('Crate properties file'){
        writeFile file: 'test-inputs.properties', text: "readCode=$read_code\nmemberCode=$member_code\nsearchValue=$search_value\norcidId=$orcid_id\n"
    }
    
    stage('Prepare Environment'){
        sh "rm -rf .py_env results"
        sh "virtualenv .py_env"
        sh "mkdir results"
        sh ". .py_env/bin/activate && pip2 install -r ./requirements.txt"
    }
    
    stage('Run Test'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_public_api_read_search.xml test_public_api_read_search.py"
            sh ". .py_env/bin/activate && py.test --junitxml results/test_member_api_post_update.xml test_member_api_post_update.py"
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        } finally {
            junit 'results/*.xml'
        }
    }
}