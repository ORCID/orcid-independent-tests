# orcid-independent-tests

## Overview

This project uses automated calls to test ORCID API functionality.

The tests are divided into two group Step 1 tests read and write to static records on QA but the records are not changed as any written information is then deleted. Step 2 tests update a given ORCID record and can not be run twice on the same record.

### Step one tests (no updates)

* test_public_record.py : test reading public information
* test_limited_record.py : test reading limited information
* test_private_record.py : test that private items are not returned
* test_VERSIONapi_all_endpoints.py : test post, put, read and delete for every API endpoint
* test_scope_methods : test that API scopes behave as expected
* test_read_endpoints : test reading every endpoint

### Step two tests (update a record)
 * test_memberVERSION_api_post_update : Post items to a record
 * test_public_api_read_search : test the record is in search results

## Setup

* [Install python 2.7.17](https://www.python.org/downloads/release/python-2717/) (make sure to include pip and add to environment variables)
* Download the independent tests source code
* Navigate to the orcid folder within the source and run 'pip install -r requirements.txt'

## Dev Environment Setup

Before executing the test suite prepare a virtual enviroment using the next commands

    rm -rf .py_env results *.secret
    mkdir results
    virtualenv .py_env
    . .py_env/bin/activate
    pip2 install -r ./orcid/requirements.txt

## Running Tests

Each test_*.py file at _orcid_ folder is expecting a _properties.py_ file containing at least next key values

    test_server=localhost.orcid.org
    user_login=ma_test_13feb2017
    password=abcxyz
    orcidId=0000-0003-4248-6064
    searchValue=13feb2017

Run the required line in the source folder to execute a given test:
  
    py.test --junitxml orcid/.py_env/Scripts/results/test_public_record.xml orcid/test_public_record.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_limited_record.xml orcid/test_limited_record.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_private_record.xml orcid/test_private_record.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_20api_all_endpoints.xml orcid/test_20api_all_endpoints.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_21api_all_endpoints.xml orcid/test_21api_all_endpoints.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_30api_all_endpoints.xml orcid/test_30api_all_endpoints.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_30api_obo_user_all_endpoints.xml orcid/test_30api_obo_user_all_endpoints.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_30rc1api_all_endpoints.xml orcid/test_30rc1api_all_endpoints.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_30rc2api_all_endpoints.xml orcid/test_30rc2api_all_endpoints.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_scope_methods.xml orcid/test_scope_methods.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_read_endpoints.xml orcid/test_read_endpoints.py

    py.test --junitxml orcid/.py_env/Scripts/results/test_member20_api_post_update.xml orcid/test_member20_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member21_api_post_update.xml orcid/test_member21_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member30_api_post_update.xml orcid/test_member30_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member30rc1_api_post_update.xml orcid/test_member30rc1_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member30rc2_api_post_update.xml orcid/test_member30rc2_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member_obo.xml orcid/test_member_obo.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_oauth_open_id.xml orcid/test_oauth_open_id.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_public_api_read_search.xml orcid/test_public_api_read_search.py

## Configure Automated Execution with Jenkins

At CI server create a job to load this repo and execute the test

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

* Thanks to the `junit` build-in method the results will be available as a report on jenkins build results

## Run automated tests on Jenkins

https://ci.orcid.org/job/ORCID-independent-tests-step1/

https://ci.orcid.org/job/ORCID-independent-tests-step2/

Click 'Build with parameters' to run each set of tests
