# orcid-independent-tests

## Overview

OrciD API privide and support data exchage using curl command line calls. This project simulate an automated call iteration.

## Required Python Libraries

* pytest
* junit-xml

Already included on _requirements.txt_ file

## Dev Environment Setup

Before executing the test suite prepare a virtual enviroment using the next commands

```
rm -rf .py_env results
mkdir results
virtualenv .py_env
. .py_env/bin/activate
pip2 install -r ./requirements.txt
```
## Running Tests

Each test_*.py file at _orcid_ folder is expecting a _properties.py_ file containing at least next key values

    test_server=localhost.orcid.org
    user_login=ma_test_13feb2017
    password=abcxyz
    orcidId=0000-0003-4248-6064
    searchValue=13feb2017

In order to execute the test suite against the target server

    source .py_env/bin/activate
    py.test --junitxml results/test_public_api_read_search.xml orcid/test_public_api_read_search.py

## Implement Automated Execution At Jenkins

At CI server lets create a job to load this repo and execute the test

* Create new job of type `pipeline`

* Inside node definition include at least next stages

```
    stage('Prepare Environment'){
        sh "rm -rf .py_env results"
        sh "virtualenv .py_env"
        sh "mkdir results"
    }
    stage('Run Test'){
        try {
            sh ". .py_env/bin/activate && pip2 install -r ./requirements.txt && py.test --junitxml results/TestLoadRecord.xml TestLoadRecord.py"
        } catch(Exception err) {
            def err_msg = err.getMessage()
            echo "Tests problem: $err_msg"
        } finally {
            junit 'results/*.xml'
        }
    }
```

[full test](http://ci-3.orcid.org:8383/job/ORCID-independent-tests)

* Thanks to the `junit` build-in method the results will be available as a report on jenkins build results


