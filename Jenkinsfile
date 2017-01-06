node {

    properties([
        buildDiscarder(
            logRotator(artifactDaysToKeepStr: '1', artifactNumToKeepStr: '2', daysToKeepStr: '', numToKeepStr: '3')), 
            [$class: 'RebuildSettings', autoRebuild: false, rebuildDisabled: false],
            pipelineTriggers([])
    ])
    
    git url: 'https://github.com/ORCID/orcid-independent-tests.git'

    stage('Prepare Environment'){
        sh "rm -rf virt results"
        sh "virtualenv virt"
        sh "mkdir results"
    }
    stage('Run Test'){
        try {
            sh ". virt/bin/activate && pip2 install -r ./requirements.txt && py.test --junitxml results/TestLoadRecord.xml TestLoadRecord.py"
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        } finally {
            junit 'results/*.xml'
        }
    }
}