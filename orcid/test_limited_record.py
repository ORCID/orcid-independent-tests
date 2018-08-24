import OrcidBaseTest
import re
import properties
import urllib

class LimitedRecord(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
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
        self.public_json_items = ['getWorkInfo.json?workId=141942', 'affiliations.json?affiliationIds=1412', 'fundings.json?fundingIds=1285']
        self.public_json_work = ['works.json?workIds=141942', 'peer-reviews.json?sortAsc=true']
        self.empty_pub_record12 = '</orcid-profile>\n</orcid-message>'

 #Test no information is returned using the public API

    def test_read_limited_record_with_20_public_api(self):
    	#TEST 139
	curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
    	response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
	response_body = response.partition('X-Frame-Options: DENY')[2]
	response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
	#Compare the body of the response to the saved file.
	self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record20.xml','r').read(), 'response_body: ' + response_body)

	def test_read_limited_record_with_21_public_api(self):
    	#TEST 139
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
    	response = self.orcid_curl("https://pub." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/record", curl_params)
    	response_body = response.partition('X-Frame-Options: DENY')[2]
    	response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
    	#Compare the body of the response to the saved file.
    	self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record21.xml','r').read(), 'response_body: ' + response_body)

	def test_read_limited_record_with_30_public_api(self):
    	#TEST 139
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
    	response = self.orcid_curl("https://pub." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/record", curl_params)
    	response_body = response.partition('X-Frame-Options: DENY')[2]
    	response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
    	#Compare the body of the response to the saved file.
    	self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record30.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_20_public_api(self):
        # TEST 140
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
		self.assertTrue("<error-code>9039</error-code>" in response, "Expected error code 9039 instead: " + response)

    def test_read_limited_email_with_20_public_api(self):
        # TEST 141
		curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
		#Check an empty email sections is returned
		self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)

    def test_read_limited_email_with_30_public_api(self):
        # TEST 141
		curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://pub." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/email", curl_params)
		#Check an empty email sections is returned
		self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)

#Test no information is returned using a read-public token on the member API
    def test_read_limited_record_with_12_public_token(self):
    	#TEST 142
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v1.2/" + self.limited_orcid_id + "/orcid-profile", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<last-modified-date\>|\<created-date\>)(.*)(\</last-modified-date\>|\</created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record12.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_record_with_20_public_token(self):
    	#TEST 143
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record20.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_20_public_token(self):
        # TEST 144
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_20_public_token(self):
        # TEST 145
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
       	#Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)

    def test_read_limited_record_with_21_public_token(self):
    	#TEST 143
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/record", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record21.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_21_public_token(self):
        # TEST 144
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_21_public_token(self):
        # TEST 145
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/email", curl_params)
       	#Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)

	def test_read_limited_funding_with_21_public_token(self):
	 	# Test nothing is returned when limited funding is read with the pulic api
	 	curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
	 	response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "funding/1285", curl_params)
	 	self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_record_with_30_public_token(self):
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/record", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record30.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_30_public_token(self):
        # TEST 144
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_30_public_token(self):
        # TEST 145
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/email", curl_params)
       	#Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)

#Test revoked access tokens can't be used to read the record
    def test_read_limited_record_with_12_revoked_token(self):
    	#TEST 146
	curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-i', '-k', '-X', 'GET']
	response = self.orcid_curl("https://api." + properties.test_server + "/v1.2/" + self.limited_orcid_id + "/orcid-profile", curl_params)
	self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_record_with_20_revoked_token(self):
    	#TEST 147
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
		self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_work_with_20_revoked_token(self):
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
		self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_email_with_20_revoked_token(self):
    	curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-i', '-k', '-X', 'GET']
    	response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
    	self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_record_with_21_revoked_token(self):
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/record", curl_params)
		self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_work_with_21_revoked_token(self):
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/work/141942", curl_params)
		self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_email_with_21_revoked_token(self):
    	curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-i', '-k', '-X', 'GET']
    	response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/email", curl_params)
    	self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_record_with_30_revoked_token(self):
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/record", curl_params)
		self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_work_with_30_revoked_token(self):
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/work/141942", curl_params)
		self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)

    def test_read_limited_email_with_30_revoked_token(self):
    	curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.revoked_token, '-L', '-i', '-k', '-X', 'GET']
    	response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/email", curl_params)
    	self.assertTrue("Invalid access token" in response, "Expected Invalid access token error, instead: " + response)


#Test access tokens for another record can't be used to read the record
    def test_read_limited_record_with_12_wrong_token(self):
    	#TEST 148
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v1.2/" + self.limited_orcid_id + "/orcid-profile", curl_params)
		self.assertTrue("You do not have the required permissions" in response, "Expected security issue error, instead: " + response)

    def test_read_limited_record_with_20_wrong_token(self):
    	#TEST 149
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
		self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_work_with_20_wrong_token(self):
        # TEST 150
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_email_with_20_wrong_token(self):
        # TEST 151
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

	def test_read_limited_record_with_21_wrong_token(self):
    	#TEST 149
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/record", curl_params)
		self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_work_with_21_wrong_token(self):
        # TEST 150
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_email_with_21_wrong_token(self):
        # TEST 151
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

	def test_read_limited_record_with_30_wrong_token(self):
    	#TEST 149
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/record", curl_params)
		self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_work_with_30_wrong_token(self):
        # TEST 150
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

    def test_read_limited_email_with_30_wrong_token(self):
        # TEST 151
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.wrong_record_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("<error-code>9017</error-code>" in response, "Expected error code 9017 instead: " + response)

#Test an update access tokens can't be used to read the record
    def test_read_limited_record_with_12_update_token(self):
    	#TEST 152
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v1.2/" + self.limited_orcid_id + "/orcid-profile", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<last-modified-date\>|\<created-date\>)(.*)(\</last-modified-date\>|\</created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record12.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_record_with_20_update_token(self):
    	#TEST 153
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record20.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_20_update_token(self):
        # TEST 154
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_20_update_token(self):
    	curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
       	#Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)

    def test_read_limited_record_with_21_update_token(self):
    	#TEST 153
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/record", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record21.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_21_update_token(self):
        # TEST 154
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_21_update_token(self):
    	curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/email", curl_params)
       	#Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)

    def test_read_limited_record_with_30_update_token(self):
    	#TEST 153
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/record", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record30.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_30_update_token(self):
        # TEST 154
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9038</error-code>" in response, "Expected error code 9038 instead: " + response)

    def test_read_limited_email_with_30_update_token(self):
    	curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.update_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/email", curl_params)
       	#Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)

#Test a create token can't be used to read the record
    def test_read_limited_record_with_12_create_token(self):
    	#TEST 155
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.create_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v1.2/" + self.limited_orcid_id + "/orcid-profile", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<last-modified-date\>|\<created-date\>)(.*)(\</last-modified-date\>|\</created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/empty_limited_record12.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_record_with_20_create_token(self):
    	#TEST 156
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.create_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
		self.assertTrue("<error-code>9005</error-code>" in response, "Expected error code 9005 instead: " + response)

    def test_read_limited_work_with_20_create_token(self):
        # TEST 157
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.create_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        self.assertTrue("<error-code>9005</error-code>" in response, "Expected error code 9005 instead: " + response)

    def test_read_limited_email_with_20_create_token(self):
    	# TEST 158
    	curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.create_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
        self.assertTrue("<error-code>9005</error-code>" in response, "Expected error code 9005 instead: " + response)

#Test an active read-limited token returns information as expected
    def test_read_limited_record_with_12_limited_token(self):
    	#TEST 159
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v1.2/" + self.limited_orcid_id + "/orcid-profile", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<last-modified-date\>|\<created-date\>)(.*)(\</last-modified-date\>|\</created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/limited_record12.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_record_with_20_limited_token(self):
    	#TEST 160
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/record", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/limited_record20.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_20_limited_token(self):
        # TEST 161
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/work/141942", curl_params)
        response_body = response.partition('X-Frame-Options: DENY')[2]
        response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_work20.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_email_with_20_limited_token(self):
    	# TEST 162
    	curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
    	response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.limited_orcid_id + "/email", curl_params)
    	response_body = response.partition('X-Frame-Options: DENY')[2]
        response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_email20.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_record_with_21_limited_token(self):
    	#TEST 160
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/record", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/limited_record21.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_21_limited_token(self):
        # TEST 161
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/work/141942", curl_params)
        response_body = response.partition('X-Frame-Options: DENY')[2]
        response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_work21.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_email_with_21_limited_token(self):
    	# TEST 162
    	curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
    	response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.limited_orcid_id + "/email", curl_params)
    	response_body = response.partition('X-Frame-Options: DENY')[2]
        response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_email21.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_record_with_30_limited_token(self):
    	#TEST 160
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/record", curl_params)
		response_body = response.partition('X-Frame-Options: DENY')[2]
		response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
		#Compare the body of the response to the saved file.
		self.assertTrue(response_body.strip() == open('saved_records/limited_record30.xml','r').read(), 'response_body: ' + response_body)

    def test_read_limited_work_with_30_limited_token(self):
        # TEST 161
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/work/141942", curl_params)
        response_body = response.partition('X-Frame-Options: DENY')[2]
        response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_work30.json','r').read(), 'response_body: ' + response_body)

    def test_read_limited_email_with_30_limited_token(self):
    	# TEST 162
    	curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
    	response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.limited_orcid_id + "/email", curl_params)
    	response_body = response.partition('X-Frame-Options: DENY')[2]
        response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_body)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open('saved_records/limited_record_email30.json','r').read(), 'response_body: ' + response_body)


#Test public json expecting server errors
    def test_limited_public_json_server_error(self):
        for item in self.public_json_items:
            work_url = ('http://qa.orcid.org/' + self.limited_orcid_id + '/' + item)
            response = urllib.urlopen(work_url).read()
            print work_url
            self.assertTrue("There has been a problem with the server" in response, "Expected server error instead: " + response)

#Test public json expecting empty page
    def test_limited_public_json_empty(self):
        for item in self.public_json_work:
            work_url = ('http://qa.orcid.org/' + self.limited_orcid_id + '/' + item)
            response = urllib.urlopen(work_url).read()
            print work_url
            self.assertTrue("[]" in response, "Expected empty brackets instead: " + response)
