# orcid-independent-tests

## Overview

Orcid API privide and support data exchage using curl command line calls. This project simulate an automated call iteration.

## Required Python Libraries

* pytest
* junit-xml
* pyjavaproperties

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

Each test_*.py test on python folder is expecting a _test.properties_ file containing at least next key values

    publicClientId=APP-AAAAAAAAAAAAAAAA
    memberClientId=APP-BBBBBBBBBBBBBBBB
    premiumClientId=APP-CCCCCCCCCCCCCCC
    publicClientSecret=FFFFFFFF-AAAA-BBBB-CCCC-GGGGGGGGGGGG
    memberClientSecret=FFFFFFFF-AAAA-BBBB-CCCC-GGGGGGGGGGGG
    premiumClientSecret=FFFFFFFF-AAAA-BBBB-CCCC-GGGGGGGGGGGG
    searchValue=family-name:13jan2017
    orcidId=0000-0003-4248-6064
    readPublicCode=123456
    api1PostUpdateCode=a1b2c3
    api2PostUpdateCode=x9y8z7

To get the 3 codes above you'll need to browse next urls

* public read api (test 40)
    * https://qa.orcid.org/oauth/authorize?client_id=[public client id]&response_type=code&scope=/authenticate&redirect_uri=https://developers.google.com/oauthplayground
* api 1.2 post update (test 53)
    * https://qa.orcid.org/oauth/authorize?client_id=[member client id]&response_type=code&scope=/orcid-bio/update /orcid-works/create /orcid-works/update /affiliations/create /affiliations/update /funding/create /funding/update /orcid-profile/read-limited&redirect_uri=https://developers.google.com/oauthplayground&email=ma_test_[DD][month][YYYY]@mailinator.com
* api 2 post update (test 80)
    * https://qa.orcid.org/oauth/authorize?client_id=[member client id]&response_type=code&scope=/read-limited /activities/update /person/update&redirect_uri=https://developers.google.com/oauthplayground

In order to execute the test suite against the target urls

    py.test --junitxml results/TestLoadRecord.xml python/TestLoadRecord.py

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


