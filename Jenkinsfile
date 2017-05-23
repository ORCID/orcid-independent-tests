node {

    properties([
        buildDiscarder(
            logRotator(artifactDaysToKeepStr: '5', artifactNumToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
        ),
        parameters([
            string(name: 'branch_to_build'       , defaultValue: 'master'                                         , description: 'Branch name to work on'),
            string(name: 'user_login'            , defaultValue: 'ma_test_23feb2017'                              , description: 'Username'),
            string(name: 'user_pass'             , defaultValue: 's$Y44853Wu3W'                                   , description: 'Password'),
            string(name: 'orcid_id'              , defaultValue: '0000-0001-6143-7896'                            , description: 'Latest orcid ID'),
            string(name: 'search_value'          , defaultValue: '23feb2017'                                      , description: 'Family name query format'),            
            string(name: 'client_secrets_file'   , defaultValue: '/var/lib/jenkins/orcidclients.py'               , description: 'Properties file with predefined secrets')
        ]),        
        [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false]
    ])
    
    git url: 'https://github.com/ORCID/orcid-independent-tests.git', branch: params.branch_to_build
    
    stage('Crate properties file'){
        sh "rm -f orcid/properties.py"
        writeFile file: 'testinputs.py', text: "searchValue=$search_value\norcidId=$orcid_id\nuser_login=$user_login\npassword=$user_pass\n"
        sh "cat $client_secrets_file testinputs.py > orcid/properties.py"
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
    
    stage('Run Test Public Record'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_public_record.xml orcid/test_public_record.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    
    stage('Run Test Private Record'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_private_record.xml orcid/test_private_record.py"
            
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
    
    stage('Run Limited Record Test'){
        try {
            
            sh ". .py_env/bin/activate && py.test --junitxml results/test_limited_record.xml orcid/test_limited_record.py"
            
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
