node {

    properties([
        buildDiscarder(
            logRotator(artifactDaysToKeepStr: '5', artifactNumToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
        ),
        parameters([
            string(name: 'branch_to_build'       , defaultValue: 'tests_coding'                                   , description: 'Branch name to work on'),            
            string(name: 'orcid_id'              , defaultValue: '0000-0003-4248-6064'                            , description: 'Latest orcid id'),
            string(name: 'search_value'          , defaultValue: 'family-name:13jan2017'                          , description: 'Username suffix to search'),
            string(name: 'read_code'             , defaultValue: 'xHvV5b'                                         , description: 'Six digits code with read privileges'),
            string(name: 'api1_code'             , defaultValue: '53Z20x'                                         , description: 'Six digits code with post/update privileges for API 1.2'),
            string(name: 'api2_code'             , defaultValue: 'YM8UAE'                                         , description: 'Six digits code with post/update privileges for API 2.0'),
            string(name: 'client_secrets_file'   , defaultValue: '/var/lib/jenkins/test.properties'               , description: 'Properties file with predefined secrets')
        ]),        
        [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false]
    ])
    
    git url: 'https://github.com/ORCID/orcid-independent-tests.git', branch: params.branch_to_build
    
    stage('Crate properties file'){
        sh "rm -f *.properties"
        writeFile file: 'test-inputs.properties', text: "searchValue=$search_value\norcidId=$orcid_id\nreadPublicCode=$read_code\napi1PostUpdateCode=$api1_code\napi2PostUpdateCode=$api2_code"
        sh "cat $client_secrets_file test-inputs.properties > test.properties"
    }
    
    stage('Prepare Environment'){
        sh "rm -rf .py_env results"
        sh "virtualenv .py_env"
        sh "mkdir results"
        sh ". .py_env/bin/activate && pip2 install -r python/requirements.txt"
    }
    
    stage('Run Test'){
        try {
        
            sh ". .py_env/bin/activate && py.test --junitxml results/test_public_api_read_search.xml python/test_public_api_read_search.py"
            
            sh ". .py_env/bin/activate && py.test --junitxml results/test_member12_api_post_update.xml python/test_member12_api_post_update.py"
            
            sh ". .py_env/bin/activate && py.test --junitxml results/test_member20_api_post_update.xml python/test_member20_api_post_update.py"
            
            sh ". .py_env/bin/activate && py.test --junitxml results/test_scope_methods.xml python/test_scope_methods.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        } finally {
            junit 'results/*.xml'
        }
    }
}