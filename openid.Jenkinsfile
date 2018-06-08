node {

    properties([
        buildDiscarder(
            logRotator(artifactDaysToKeepStr: '5', artifactNumToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
        ),
        parameters([
            string(name: 'branch_to_build'       , defaultValue: 'master'        , description: 'Branch name to work on'),
            string(name: 'test_server'           , defaultValue: 'qa.orcid.org'  , description: 'Base domain name to test'),
            string(name: 'user_login'            , defaultValue: ''              , description: 'Username'),
            string(name: 'user_pass'             , defaultValue: ''              , description: 'Password'),
            string(name: 'user_orcid_id'         , defaultValue: ''              , description: 'Latest orcid ID'),
            string(name: 'user_api_id'           , defaultValue: ''              , description: 'Client ID'),
        ]),
        [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false]
    ])

    git url: 'https://github.com/ORCID/orcid-independent-tests.git', branch: params.branch_to_build

    stage('Build properties file'){
        sh "rm -f orcid/properties.py"
        writeFile file: 'testinputs.py', text: "test_server=\"$test_server\"\nuser_orcid_id=\"$user_orcid_id\"\nuser_login=\"$user_login\"\nuser_pass=\"$user_pass\"\nuser_api_id=\"$user_api_id\"\n"
        sh "cat /var/lib/jenkins/orcidclients.py testinputs.py > orcid/properties.py"
    }

    stage('Prepare Environment'){
        sh "rm -rf .py_env results"
        sh "virtualenv .py_env"
        sh "mkdir results"
        sh ". .py_env/bin/activate && pip2 install -r orcid/requirements.txt"
    }

    stage('Run OpenID Tests'){
        try {
            sh ". .py_env/bin/activate && py.test --junitxml results/test_oauth_open_id.xml orcid/test_oauth_open_id.py"
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        }
    }
}
