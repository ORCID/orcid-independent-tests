# orcid-independent-tests

## Overview

Orcid API privide and support data exchage using curl command line calls. This project simulate an automated call iteration.

## Required Python Libraries

* pytest
* junit-xml

Already included on requirements.txt file

## Dev Environment Setup

Before executing the test suite prepare a virtual enviroment using the next commands

```
rm -rf orcid results
mkdir results
virtualenv orcid
. orcid/bin/activate
pip2 install -r ./requirements.txt
```
## Running Tests

In order to execute the test suite against the target urls

    py.test --junitxml results/TestLoadRecord.xml TestLoadRecord.py

## Implement Automated Execution At Jenkins

At CI server lets create a job to load this repo and execute the test

* Create new job of type `pipeline`

* Inside node definition include at least next stages

```
    stage('Prepare Environment'){
        sh "rm -rf orcid results"
        sh "virtualenv orcid"
        sh "mkdir results"
    }
    stage('Run Test'){
        try {
            sh ". orcid/bin/activate && pip2 install -r ./requirements.txt && py.test --junitxml results/TestLoadRecord.xml TestLoadRecord.py"
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        } finally {
            junit 'results/*.xml'
        }
    }
```

* Thanks to the `junit` build-in method the results will be available as a report on jenkins build results


