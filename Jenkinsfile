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
        sh ". virt/bin/activate && pip2 install -r ./requirements.txt && py.test --junitxml results/TestLoadRecord.xml TestLoadRecord.py"
    }
    stage('Save Test Results'){
        junit 'results/*.xml'
    }
}