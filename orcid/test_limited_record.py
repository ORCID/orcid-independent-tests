import OrcidBaseTest
import re
import properties
import urllib
import local_properties

class LimitedRecord(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        if properties.type == "actions":
          self.test_server = properties.test_server
        else:
          self.test_server = local_properties.test_server
        self.limited_orcid_id = '0000-0001-7325-5491'
        self.limited_token = '1fcda8a0-1af3-4b35-8825-e4c53dae8953'
        self.public_token = 'ba290a09-b757-4583-a5af-bd55d7087467'
        self.public_api_token = '80e4aa5a-6ccc-44b3-83bb-3d9e315cda22'
        self.revoked_token = '63409312-5ef6-4051-988c-f33b0fcea09f'
        self.wrong_record_token = '2283056e-6a4a-4c80-b3a0-beaa102161d0'
        self.update_token = '064e64ef-6c49-4634-b09b-a38d8d75c774'
        self.create_token = 'ddc95880-fbfb-4fbf-931e-a18e15cf0a1c'
        self.empty_email = '"email":[]'
        self.activities = ['educations', 'employments', 'fundings', 'works', 'peer-reviews']
        self.bio_sections2 = ['other-name', 'researcher-url', 'keyword', 'external-identifier', 'email', 'address']
        self.public_json_items = ['getWorkInfo.json?workId=141942', 'affiliations.json?affiliationIds=1412']
        self.public_json_work = ['works.json?workIds=141942', 'peer-reviews.json?sortAsc=true', 'fundingGroups.json?sort=date&sortAsc=true']
        self.empty_pub_record12 = '</orcid-profile>\n</orcid-message>'

    def getResponse(self, response):
       return re.sub('[    ](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\n','', response)
     
    #Test no information is returned using the public API
    def test_read_limited_record_with_20_public_api(self):
        #Test that reading a limited record with the 2.0 public api returns only the public info
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        saved_file = open('saved_records/empty_limited_record20.xml','r').read()
        self.assertTrue(response_body.strip() == saved_file, 'response_body: ' + response_body.strip() + 'saved_file: ' + saved_file)

    def test_read_limited_record_with_21_public_api(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record21.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_record_with_30_rc1_public_api(self):
        #Test that reading a limited record with the 3.0 public api returns only the public info
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record30_rc1.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_record_with_30_rc2_public_api(self):
        #Test that reading a limited record with the 3.0_rc2 public api returns only the public info
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record30_rc2.xml','r').read(), 'response_body: ' + response_body)


    def test_read_limited_record_with_30_public_api(self):
        #Test that reading a limited record with the 3.0 public api returns only the public info
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record30.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_20_public_api(self):
        # Test read limited work with the public api and make sure it returns error 9039
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9039</error-code>" in response, "Expected error code 9039 instead: " + response)

    def test_read_limited_work_with_21_public_api(self):
        # Test read limited work with the public api and make sure it returns error 9039
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9039</error-code>" in response, "Expected error code 9039 instead: " + response)

    def test_read_limited_work_with_30_public_api(self):
        # Test read limited work with the public api and make sure it returns error 9039
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9039</error-code>" in response, "Expected error code 9039 instead: " + response)

    def test_read_limited_email_with_20_public_api(self):
        # Test read the limted record email make sure it doesn't return anything
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)

    def test_read_limited_email_with_21_public_api(self):
        # Test read the limited record email make sure it doesn't return anything
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_limited_email_with_30_rc1_public_api(self):
        # Test no info is returned when the reading limited record email ewith the 3.0_rc1 public api
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_limited_email_with_30rc2_public_api(self):
        # Test no info is returned when the reading limited record email with the 3.0_rc2 public api
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_limited_email_with_30_public_api(self):
        # Test no info is returned when the reading limited record email with the 3.0 public api
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_limited_record_with_20_public_token(self):
        #Test that reading a limited record with the 2.0 public api returns only the public info
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record20.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_20_public_token(self):
        # Test read limited work with the 2.0 public api and make sure it returns error 9039
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_20_public_token(self):
        # Test no info is returned when the reading limited record email with the 2.0 public api
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
       	#Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_limited_funding_with_20_public_token(self):
        # Test nothing is returned when limited funding is read with the public api
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/funding/1285", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_record_with_21_public_token(self):
        #Test that reading a limited record with the 2.1 public api returns only the public info
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record21.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_21_public_token(self):
        # TEST 144
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_21_public_token(self):
        # TEST 145
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_limited_funding_with_21_public_token(self):
        # Test nothing is returned when limited funding is read with the public api
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/funding/1285", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_record_with_30_rc1_public_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record30_rc1.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_30_rc1_public_token(self):
        # TEST 144
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_30_rc1_public_token(self):
        # TEST 145
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)


    def test_read_limited_funding_with_30_rc1_public_token(self):
        # Test nothing is returned when limited funding is read with the public api
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/funding/1285", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_record_with_30rc2_public_token(self):
    #Test when limited record is read with the 3.0_rc2 public api it matches the saved file
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record30_rc2.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_30rc2_public_token(self):
        #Test 9038 error  is returned when limited work is read with the 3.0_rc2 public api
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_30rc2_public_token(self):
        # TEST 145
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_limited_funding_with_30rc2_public_token(self):
        # Test nothing is returned when limited funding is read with the public api
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/funding/1285", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_record_with_30_public_token(self):
        # Test when limited record is read with the 3.0 public api it matches the saved file
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        # Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record30.xml', 'r').read(),'response_body: ' + response_body)

    def test_read_limited_work_with_30_public_token(self):
        # Test 9038 error  is returned when limited work is read with the 3.0 public api
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_30_public_token(self):
        # TEST 145
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/email",curl_params)
        # Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_limited_funding_with_30_public_token(self):
        # Test nothing is returned when limited funding is read with the public api
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/funding/1285", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_record_with_20_revoked_token(self):
        #TEST 147
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_work_with_20_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_email_with_20_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_record_with_21_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/record", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_work_with_21_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_email_with_21_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_record_with_30_rc1_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/record", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_work_with_30_rc1_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_email_with_30_rc1_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_record_with_30rc2_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/record", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_work_with_30rc2_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_email_with_30rc2_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_record_with_30_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/record", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_work_with_30_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_email_with_30_revoked_token(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_record_with_20_wrong_token(self):
        #TEST 149
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_work_with_20_wrong_token(self):
        # TEST 150
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_email_with_20_wrong_token(self):
        # TEST 151
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_record_with_21_wrong_token(self):
        #TEST 149
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/record", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_work_with_21_wrong_token(self):
        # TEST 150
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_email_with_21_wrong_token(self):
        # TEST 151
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_record_with_30_rc1_wrong_token(self):
        #TEST 149
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/record", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_work_with_30_rc1_wrong_token(self):
        # TEST 150
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_email_with_30_rc1_wrong_token(self):
        # TEST 151
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_record_with_30rc2_wrong_token(self):
        #TEST 149
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/record",     curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_work_with_30rc2_wrong_token(self):
        # TEST 150
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_email_with_30rc2_wrong_token(self):
        # TEST 151
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_record_with_30_wrong_token(self):
        #TEST 149
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/record",     curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_work_with_30_wrong_token(self):
        # TEST 150
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/work/141942",   curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_email_with_30_wrong_token(self):
        # TEST 151
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    #Test an update access tokens can't be used to read the record
    def test_read_limited_record_with_20_update_token(self):
        #TEST 153
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record20.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_20_update_token(self):
        # TEST 154
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_20_update_token(self):
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_limited_record_with_21_update_token(self):
        #TEST 153
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L',  '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record21.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_21_update_token(self):
        # TEST 154
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_21_update_token(self):
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_limited_record_with_30_rc1_update_token(self):
        #TEST 153
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record30_rc1.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_30_rc1_update_token(self):
        # TEST 154
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_30_rc1_update_token(self):
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_limited_record_with_30rc2_update_token(self):
        #TEST 153
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L',  '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record30_rc2.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_30rc2_update_token(self):
      # TEST 154
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/work/141942", curl_params)
      self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_30rc2_update_token(self):
      curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.update_token, '-L','-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/email", curl_params)
      # Check an empty email sections is returned
      self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_limited_record_with_30_update_token(self):
        #TEST 153
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record30.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_30_update_token(self):
        # TEST 154
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-k', '-X',   'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/work/141942",   curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_30_update_token(self):
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/email", curl_params)
            #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    #Test a create token can't be used to read the record

    def test_read_limited_record_with_20_create_token(self):
        #TEST 156
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.create_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
        self.assertTrue("<error-code>9005</error-code>" in response, "Expected error code 9005 instead: " + response)

    def test_read_limited_work_with_20_create_token(self):
        # TEST 157
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.create_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9005</error-code>" in response, "Expected error code 9005 instead: " + response)

    def test_read_limited_email_with_20_create_token(self):
        # TEST 158
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.create_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("<error-code>9005</error-code>" in response, "Expected error code 9005 instead: " + response)

    #Test an active read-limited token returns information as expected
    def test_read_limited_record_with_20_limited_token(self):
        #TEST 160
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record20.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_20_limited_token(self):
        # TEST 161
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_work20.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_email_with_20_limited_token(self):
        # TEST 162
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_email20.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_record_with_21_limited_token(self):
        #TEST 160
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record21.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_21_limited_token(self):
        # TEST 161
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/work/141942", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_work21.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_email_with_21_limited_token(self):
        # TEST 162
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/email", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_email21.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_record_with_30_rc1_limited_token(self):
        #TEST 160
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record30_rc1.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_30_rc1_limited_token(self):
        # TEST 161
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/work/141942", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_work30_rc1.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_email_with_30_rc1_limited_token(self):
        # TEST 162
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/email", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_email30_rc1.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_record_with_30_rc2_limited_token(self):
        #TEST 160
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record30_rc2.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_30rc2_limited_token(self):
        # TEST 161
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/work/141942", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_work30_rc2.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_email_with_30rc2_limited_token(self):
        # TEST 162
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/email", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_email30_rc2.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_record_with_30_limited_token(self):
        #TEST 160
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record30.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_30_limited_token(self):
        # TEST 161
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_work30.json','r').read(), 'response_body: ' + response_body)


    def test_read_limited_email_with_30_limited_token(self):
        # TEST 162
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/email", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_email30.json','r').read(), 'response_body: ' + response_body)

    #Test public json expecting server errors
    def test_limited_public_json_server_error(self):
        for item in self.public_json_items:
            work_url = ("http://" + self.test_server + '/' + self.limited_orcid_id + '/' + item)
            response = urllib.urlopen(work_url).read()
            print (work_url)
            self.assertTrue("There has been a problem with the server" in response, "Expected server error instead: " + response)

    #Test public json expecting empty page
    def test_limited_public_json_empty(self):
        for item in self.public_json_work:
            work_url = ("http://" + self.test_server + '/' + self.limited_orcid_id + '/' + item)
            response = urllib.urlopen(work_url).read()
            print (work_url)
            self.assertTrue("[]" == response, "Expected empty brackets instead: " + response)

    #Test public json on research-resources
    def test_limited_public_json_empty(self):
        work_url = "http://" + self.test_server + "/0000-0001-7325-5491/researchResourcePage.json?offset=0&sort=endDate&sortAsc=false&researchResourceID=1005"
        response = urllib.urlopen(work_url).read()
        print (work_url)
        self.assertTrue('{"nextOffset":50,"totalGroups":0,"groups":[]}' in response, "Expected empty brackets instead: " + response)

    # ********************************************** OBO

    # Check if the work has been posted on behalf of another member
    def test_member_obo_rc2(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/works/179580", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue("<common:assertion-origin-client-id>" in response_body, 'response_body: ' + response_body)

    # Check if the work has been posted on behalf of another member
    def test_member_obo_30(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/works/179580", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue("<common:assertion-origin-client-id>" in response_body, 'response_body: ' + response_body)

    # Assertion / Member OBO tag should be missing from releases prior to 3.0_rc2
    def test_member_obo_rc1(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/works/179580", curl_params)
        response_body = self.getResponse(response)
        assertionTag = '<common:assertion-origin-client-id>'
        workTag = '<work:work put-code="179580" visibility="limited">'
        #Compare the body of the response to the saved file.
        self.assertTrue(assertionTag not in response_body and workTag in response_body, 'response_body: ' + response_body)

    # Assertion / Member OBO tag should be missing from releases prior to 3.0_rc2
    def test_member_obo_20(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/works/179580", curl_params)
        response_body = self.getResponse(response)
        assertionTag = '<common:assertion-origin-client-id>'
        workTag = '<work:work put-code="179580" visibility="limited">'
        #Compare the body of the response to the saved file.
        self.assertTrue(assertionTag not in response_body and workTag in response_body, 'response_body: ' + response_body)

    # Assertion / Member OBO tag should be missing from releases prior to 3.0_rc2
    def test_member_obo_21(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.limited_orcid_id + "/works/179580", curl_params)
        response_body = self.getResponse(response)
        assertionTag = '<common:assertion-origin-client-id>'
        workTag = '<work:work put-code="179580" visibility="limited">'
        #Compare the body of the response to the saved file.
        self.assertTrue(assertionTag not in response_body and workTag in response_body, 'response_body: ' + response_body)

    # Check if the work has been posted on behalf of another member
    def test_user_obo_rc2(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.limited_orcid_id + "/works/179625", curl_params)
        response_body = self.getResponse(response)
        assertionTag = '<common:assertion-origin-orcid>'
        originNameTag = '<common:assertion-origin-name>'
        #Compare the body of the response to the saved file.
        self.assertTrue(assertionTag in response_body and originNameTag not in response_body, 'response_body: ' + response_body)

    # Check if the work has been posted on behalf of another member
    def test_user_obo_30(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.limited_orcid_id + "/works/179625", curl_params)
        response_body = self.getResponse(response)
        assertionTag = '<common:assertion-origin-orcid>'
        originNameTag = '<common:assertion-origin-name>'
        #Compare the body of the response to the saved file.
        self.assertTrue(assertionTag in response_body and originNameTag not in response_body, 'response_body: ' + response_body)

    # Assertion / User OBO tag should be missing from releases prior to 3.0_rc2
    def test_user_obo_rc1(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/works/179625", curl_params)
        response_body = self.getResponse(response)
        assertionTag = '<common:assertion-origin-orcid>'
        workTag = '<work:work put-code="179625" visibility="limited">'
        #Compare the body of the response to the saved file.
        self.assertTrue(assertionTag not in response_body and workTag in response_body, 'response_body: ' + response_body)

    # Assertion / User OBO tag should be missing from releases prior to 3.0_rc2
    def test_user_obo_20(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.limited_orcid_id + "/works/179625", curl_params)
        response_body = self.getResponse(response)
        assertionTag = '<common:assertion-origin-orcid>'
        workTag = '<work:work put-code="179625" visibility="limited">'
        #Compare the body of the response to the saved file.
        self.assertTrue(assertionTag not in response_body and workTag in response_body, 'response_body: ' + response_body)

    # Assertion / User OBO tag should be missing from releases prior to 3.0_rc2
    def test_user_obo_21(self):
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/works/179625", curl_params)
        response_body = self.getResponse(response)
        assertionTag = '<common:assertion-origin-orcid>'
        workTag = '<work:work put-code="179625" visibility="limited">'
        #Compare the body of the response to the saved file.
        self.assertTrue(assertionTag not in response_body and workTag in response_body, 'response_body: ' + response_body)
