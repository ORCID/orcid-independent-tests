# orcid-independent-tests

This project uses automated calls to test ORCID API functionality.

The tests are divided into two group Step 1 tests read and write to static records on QA but the records are not changed as any written information is then deleted. Step 2 tests update a given ORCID record and can not be run twice on the same record.

## Local setup

* [Install python 2.7.17](https://www.python.org/downloads/release/python-2717/) (make sure to include pip and (win) add to environment variables)
* Clone the independent tests repository
* Navigate to the orcid folder within the source and run 'pip install -r requirements.txt'

Before executing the test suite prepare a virtual enviroment using the next commands

    rm -rf .py_env results *.secret
    mkdir results
    virtualenv .py_env
    . .py_env/bin/activate
    pip2 install -r ./orcid/requirements.txt

## Running tests locally

In order to run the tests locally:

* (Win) Download [geckodriver](https://github.com/mozilla/geckodriver/releases) and copy the extracted executable into your Python folder
* Change the `firefoxPath` variable in the `orcid\local_properties.py` file to point to your local Firefox folder.
* Change the `type` variable in the `orcid\local_properties.py` file to anything but "jenkins" (make sure to change back to "jenkins" when making commits)

Run the required line in the source folder to execute a given test:

### Step 1
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
    py.test --junitxml orcid/.py_env/Scripts/results/test_public_api_read_search.xml orcid/test_public_api_read_search.py
### Step 2
    py.test --junitxml orcid/.py_env/Scripts/results/test_member20_api_post_update.xml orcid/test_member20_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member21_api_post_update.xml orcid/test_member21_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member30_api_post_update.xml orcid/test_member30_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member30rc1_api_post_update.xml orcid/test_member30rc1_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member30rc2_api_post_update.xml orcid/test_member30rc2_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member_obo.xml orcid/test_member_obo.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_oauth_open_id.xml orcid/test_oauth_open_id.py


## Running tests on Jenkins

### Step 1

1. Visit the [step 1 pipeline page](https://ci.orcid.org/job/ORCID-independent-tests-step1/) and click 'Build with parameters' on the left hand side
2. Change the 'branch_to_build' parameter to choose the appropriate GitHub branch
3. Click 'Build'

### Step 2

1. Create a new ORCID record at https://qa.orcid.org/register (no need to verify) with the password `test1234`
2. Visit the [step 1 pipeline page](https://ci.orcid.org/job/ORCID-independent-tests-step2/) and click 'Build with parameters' on the left hand side
3. Configure `branch_to_build`, `user_login`, `orcid_id` and `search_value` accordingly
4. Click 'Build'

## Configure Automated Execution with Jenkins

1. Visit https://ci.orcid.org/view/independent-tests/ and choose the appropriate pipeline
2. Click configure on the left hand side to edit the pipeline configuration and manage test execution (admin rights required)

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
