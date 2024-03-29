# orcid-independent-tests

This project uses automated calls to test ORCID API functionality.

The tests are divided into two groups:
* Step 1 tests read and write to static records on QA, but the records are not changed as any written information is then deleted.
* Step 2 tests update a given ORCID record and can not be run twice on the same record, unless you are running the tests locally, in which case you can clean up the record by running `orcid/delete_record_contents.py`

## Local setup

* [Install the latest python 3 version](https://www.python.org/downloads/) (make sure to include pip and (win) add to environment variables)
* Clone the independent tests repository
* Install dependencies by running `pip install -r ./orcid/requirements.txt` in the source folder (alternatively see the virtual environment setup below)
* (Win) Download [geckodriver](https://github.com/mozilla/geckodriver/releases) and copy the extracted executable into your Python folder
* Create "local_properties.py" in the `./orcid` folder and populate it with contents of the "Independent test local properties" entry found in Dashlane.
* Change the `firefoxPath` and `geckodriverPath` property values in the `orcid\local_properties.py` file to point to your local Firefox/Geckodriver executables.

#### Virtual environment setup

    rm -rf .py_env results
    mkdir results
    virtualenv .py_env
    . .py_env/bin/activate
    pip2 install -r ./orcid/requirements.txt

Run the required line in the source folder to execute a given test:

### Step 1
    py.test --junitxml orcid/.py_env/Scripts/results/test_public_record.xml orcid/test_public_record.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_limited_record.xml orcid/test_limited_record.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_private_record.xml orcid/test_private_record.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_20api_all_endpoints.xml orcid/test_20api_all_endpoints.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_21api_all_endpoints.xml orcid/test_21api_all_endpoints.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_30api_all_endpoints.xml orcid/test_30api_all_endpoints.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_30api_obo_user_all_endpoints.xml orcid/test_30api_obo_user_all_endpoints.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_rc_api_filters.xml orcid/test_rc_api_filters.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_scope_methods.xml orcid/test_scope_methods.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_read_endpoints.xml orcid/test_read_endpoints.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_public_api_read_search.xml orcid/test_public_api_read_search.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_content_negotiation.xml orcid/test_content_negotiation.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_revoked_token.xml orcid/test_revoked_token.py
### Step 2
    py.test --junitxml orcid/.py_env/Scripts/results/test_member20_api_post_update.xml orcid/test_member20_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member21_api_post_update.xml orcid/test_member21_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member30_api_post_update.xml orcid/test_member30_api_post_update.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_member_obo.xml orcid/test_member_obo.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_oauth_open_id.xml orcid/test_oauth_open_id.py
    py.test --junitxml orcid/.py_env/Scripts/results/test_expected_errors.xml orcid/test_expected_errors.py


## Running and tweaking tests using Github Actions

To run the tests:

1. Visit [Github Actions](https://github.com/ORCID/orcid-independent-tests/actions/).
2. Select the appropriate step (workflow) and click the "Run workflow" button.
3. Fill in the details (if required) and run the test.(Note: step 2 requires to register a new user following indicated name format, with same name@mailinator.com email then verify that primary email)

The workflow files can be found [here](https://github.com/ORCID/orcid-independent-tests/tree/master/.github/workflows).

## Troubleshooting

`orcid/delete_record_contents.py` may be used to clean unnecessary data from the records used in step 1 and step 2 tests (if running the tests locally). Include the flag `-s` with the required step number, e.g. `-s 2`
