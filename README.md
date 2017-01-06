# orcid-independent-tests

## Overview

Orcid API privide and support data exchage using curl command line calls. This project simulate an automated call iteration.

## required python libraries

* pytest
* junit-xml

Already included on requirements.txt file

## Dev Environment Setup

Before executing the test suite prepare a virtual enviroment using the next commands

```
rm -rf virt results
virtualenv virt
mkdir results
. virt/bin/activate
pip2 install -r ./requirements.txt
```

Finally execute the test suite against the target urls

    py.test --junitxml results/TestLoadRecord.xml TestLoadRecord.py

## Implement automated execution from Jenkins

At CI server lets create a job to load this repo and execute the test

* Create new job of type `pipeline`

* Inside node definition include at least next stages

```
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
```

* Thanks to the `junit` build-in method the results will be available as a report on jenkins build results


