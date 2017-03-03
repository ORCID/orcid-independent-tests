node {

    properties([
        buildDiscarder(
            logRotator(artifactDaysToKeepStr: '5', artifactNumToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
        ),
        parameters([
            string(name: 'branch_to_build'       , defaultValue: 'tests_coding'                                   , description: 'Branch name to work on'),            
            string(name: 'orcid_id'              , defaultValue: '0000-0001-6143-7896'                            , description: 'Latest orcid id'),
            string(name: 'search_value'          , defaultValue: 'family-name:23feb2017'                          , description: 'Username suffix to search'),
            string(name: 'read_code'             , defaultValue: 'VIO1aT'                                         , description: 'Six digits code with /authenticate privileges'),
            string(name: 'api1_code'             , defaultValue: 'ZhtAO5'                                         , description: 'Six digits code with /orcid-bio/update /orcid-works/create /orcid-works/update /affiliations/create /affiliations/update /funding/create /funding/update /orcid-profile/read-limited scope for API 1.2'),
            string(name: 'api2_code'             , defaultValue: 'EX1Qn8'                                         , description: 'Six digits code with /read-limited /activities/update /person/update scope for API 2.0'),
            string(name: 'email_code'            , defaultValue: '3eRYEm'                                         , description: 'Six digits code with /read-limited /email/read-private scope'),
            string(name: 'client_secrets_file'   , defaultValue: '/var/lib/jenkins/test.properties'               , description: 'Properties file with predefined secrets')
        ]),        
        [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false]
    ])
    
    git url: 'https://github.com/ORCID/orcid-independent-tests.git', branch: params.branch_to_build
    
    stage('Crate properties file'){
        sh "rm -f *.properties"
        writeFile file: 'test-inputs.properties', text: "searchValue=$search_value\norcidId=$orcid_id\nreadPublicCode=$read_code\napi1PostUpdateCode=$api1_code\napi2PostUpdateCode=$api2_code\nemailCode=$email_code"
        sh "cat $client_secrets_file test-inputs.properties > test.properties"
    }
    
    stage('Prepare Environment'){
        sh "rm -rf .py_env results"
        sh "virtualenv .py_env"
        sh "mkdir results"
        sh ". .py_env/bin/activate && pip2 install -r orcid/requirements.txt"
    }
    
    stage('Clean OrcidiD'){
        sh ". .py_env/bin/activate && pytest -v -r fEx orcid/api_read_delete.py"
    }
    
    stage('Run Test Public Read'){
        try {
        
            sh ". .py_env/bin/activate && py.test --junitxml results/test_public_api_read_search.xml orcid/test_public_api_read_search.py"
                        
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    stage('Run Test 1.2 post'){
        try {
                    
            sh ". .py_env/bin/activate && py.test --junitxml results/test_member12_api_post_update.xml orcid/test_member12_api_post_update.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    stage('Run Test 2.0 post'){
        try {
            
            sh ". .py_env/bin/activate && py.test --junitxml results/test_member20_api_post_update.xml orcid/test_member20_api_post_update.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    stage('Run Test scope methods'){
        try {
            
            //sh ". .py_env/bin/activate && py.test --junitxml results/test_email_read_private.xml orcid/test_email_read_private.py"            
            sh ". .py_env/bin/activate && py.test --junitxml results/test_scope_methods.xml orcid/test_scope_methods.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        } finally {
            junit 'results/*.xml'
        }
    }    
}