import OrcidBaseTest
import properties

class PrivateRecord(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.public_token = 'ba290a09-b757-4583-a5af-bd55d7087467'
        self.public_api_token = '80e4aa5a-6ccc-44b3-83bb-3d9e315cda22'
        self.private_orcid_id = '0000-0003-2366-2712'
        self.limited_token = '6ae41a5b-abf9-4922-bbb4-08ed8508b4ce'
        self.empty_activities = '"orcid-activities":null'
        self.empty_bio = '"orcid-bio":null'
        self.empty_email = '"email":[]'
        self.activities = ['educations', 'employments', 'fundings', 'works', 'peer-reviews']
        self.bio_sections2 = ['other-name', 'researcher-url', 'keyword', 'external-identifier', 'email', 'address']

    def test_read_private_record_with_20_public_api(self):
    	# Test reading a private record with the 2.0 public API
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/" + self.private_orcid_id + "/record", curl_params)
		#Check the name and email address are not returned anywhere
        self.assertFalse('Published Name' in response, "Name returned " + response)
        self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
		#Check each bio and activities section is returned without content
        for bio_section in self.bio_sections2:
        	if bio_section == 'email':
	        	self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
	        elif bio_section == 'address':
	        	self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
	        else:
	        	self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
        for activity in self.activities:
	        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

    def test_read_private_record_with_21_public_api(self):
    	# Test reading a private record with the 2.1 public API
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.1/" + self.private_orcid_id + "/record", curl_params)
		#Check the name and email address are not returned anywhere
        self.assertFalse('Published Name' in response, "Name returned " + response)
        self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
		#Check each bio and activities section is returned without content
        for bio_section in self.bio_sections2:
        	if bio_section == 'email':
	        	self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
	        elif bio_section == 'address':
	        	self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
	        else:
	        	self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
        for activity in self.activities:
	        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

	def test_read_private_record_with_30_public_api(self):
		# Test reading a private record with the 3.0 public API
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://pub." + properties.test_server + "/v3.0_rc1/" + self.private_orcid_id + "/record", curl_params)
		#Check the name and email address are not returned anywhere
		self.assertFalse('Published Name' in response, "Name returned " + response)
		self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
		#Check each bio and activities section is returned without content
		for bio_section in self.bio_sections2:
			if bio_section == 'email':
				self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
			elif bio_section == 'address':
				self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
			else:
				self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
		for activity in self.activities:
			self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)


    def test_read_private_record_with_12_limited_token(self):
		# Test reading a private record with the 1.2 API and a limited token
		curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v1.2/" + self.private_orcid_id + "/orcid-profile", curl_params)
		#Check the name and email address are not returned anywhere
		self.assertFalse('Published Name' in response, "Name returned " + response)
		self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
		#Check an empty activities sections is returned
		self.assertTrue(self.empty_activities in response, "Non-empty activities returned " + response)
        #Unable to assert empty biography sections because it can't read text in curly brackets
        #self.assertTrue('"family-name":null' in response, "Non-empty bio returned " + response)

    def test_read_private_record_with_20_limited_token(self):
    	# Test reading a private record with the 2.0 API and a limited token
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.private_orcid_id + "/record", curl_params)
		#Check the name and email address are not returned anywhere
        self.assertFalse('Published Name' in response, "Name returned " + response)
        self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
		#Check each bio and activities section is returned without content
        for bio_section in self.bio_sections2:
        	if bio_section == 'email':
	        	self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
	        elif bio_section == 'address':
	        	self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
	        else:
	        	self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
        for activity in self.activities:
	        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

    def test_read_private_record_with_21_limited_token(self):
    	# Test reading a private record with the 2.1 API and a limited token
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.private_orcid_id + "/record", curl_params)
		#Check the name and email address are not returned anywhere
        self.assertFalse('Published Name' in response, "Name returned " + response)
        self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
		#Check each bio and activities section is returned without content
        for bio_section in self.bio_sections2:
        	if bio_section == 'email':
	        	self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
	        elif bio_section == 'address':
	        	self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
	        else:
	        	self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
        for activity in self.activities:
	        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

	def test_read_private_record_with_30_limited_token(self):
		# Test reading a private record with the 3.0 API and a limited token
		curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
		response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.private_orcid_id + "/record", curl_params)
		#Check the name and email address are not returned anywhere
		self.assertFalse('Published Name' in response, "Name returned " + response)
		self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
		#Check each bio and activities section is returned without content
		for bio_section in self.bio_sections2:
			if bio_section == 'email':
				self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
			elif bio_section == 'address':
				self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
			else:
				self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
		for activity in self.activities:
			self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

#2.0 tests

    def test_read_private_work_with_20_limited_token(self):
        # Test reading a private work with the 2.0 API and a limited token
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.private_orcid_id + "/work/141943", curl_params)
        self.assertTrue("<error-code>9013</error-code>" in response, "Expected error code 9013 instead: " + response)

    def test_read_private_email_with_20_limited_token(self):
        # Test reading a private email with the 2.0 API and a limited token
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.private_orcid_id + "/email", curl_params)
       	#Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)

    def test_read_deactivated_record_member_api_20(self):
		# Test reading a deactivated record with the member 2.0 API
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/0000-0002-7564-3444/record", curl_params)
        response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2]
       	#Check record has deactivated date
        self.assertTrue(response_body.strip() == open('saved_records/deactivated_record20.xml','r').read(), "No deactivate date " + response_body.strip() +
        "/nFile contents: /n" + open('saved_records/deactivated_record20.xml','r').read())

    def test_read_deactivated_record_public_api_20(self):
		# Test reading a deactivated record with the pubic 2.0 API
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/0000-0002-7564-3444/record", curl_params)
        response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2]
       	#Check record has deactivated date
        self.assertTrue(response_body.strip() == open('saved_records/deactivated_record20.xml','r').read(), "No deactivate date " + response_body.strip())

    def test_read_locked_record_member_api_20(self):
		# Test reading a locked record with the member 2.0 API and check error returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/0000-0002-1871-711X/record", curl_params)
       	#Check locked error is returned
        self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_locked_record_public_api_20(self):
		# Test reading a locked record with the public 2.0 API and check error returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/0000-0002-1871-711X/record", curl_params)
       	#Check locked error is returned
        self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_deprecated_record_member_api_20(self):
		# Test reading a deprecated record with the member 2.0 API and check error returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/0000-0003-2914-7527/record", curl_params)
       	#Check locked error is returned
        self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

    def test_read_deprecated_record_public_api_20(self):
		# Test reading a deprecated record with the public 2.0 API and check error returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/0000-0003-2914-7527/record", curl_params)
       	#Check locked error is returned
        self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

#2.1 tests

    def test_read_private_work_with_21_limited_token(self):
        # Test reading a private work with the 2.1 API and a limited token
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.private_orcid_id + "/work/141943", curl_params)
        self.assertTrue("<error-code>9013</error-code>" in response, "Expected error code 9013 instead: " + response)

    def test_read_private_email_with_21_limited_token(self):
        # Test reading a private email with the 2.1 API and a limited token
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.private_orcid_id + "/email", curl_params)
       	#Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)

    def test_read_deactivated_record_member_api_21(self):
		# Test reading a deactivated record with the member 2.1 API
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/0000-0002-7564-3444/record", curl_params)
        response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2]
       	#Check record has deactivated date
        self.assertTrue(response_body.strip() == open('saved_records/deactivated_record21.xml','r').read(), "No deactivate date " + response_body.strip())

    def test_read_deactivated_record_public_api_21(self):
		# Test reading a deactivated record with the public 2.1 API
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.1/0000-0002-7564-3444/record", curl_params)
        response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2]
       	#Check record has deactivated date
        self.assertTrue(response_body.strip() == open('saved_records/deactivated_record21.xml','r').read(), "No deactivate date " + response_body.strip())

    def test_read_locked_record_member_api_21(self):
		# Test reading a locked record with the member 2.1 API and check error returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/0000-0002-1871-711X/record", curl_params)
       	#Check locked error is returned
        self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_locked_record_public_api_21(self):
		# Test reading a locked record with the public 2.1 API and check error returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.1/0000-0002-1871-711X/record", curl_params)
       	#Check locked error is returned
        self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_deprecated_record_member_api_21(self):
		# Test reading a depracated record with the member 2.1 API and check error returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/0000-0003-2914-7527/record", curl_params)
       	#Check locked error is returned
        self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

    def test_read_deprecated_record_public_api_21(self):
		# Test reading a depracated record with the public 2.1 API and check error returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.1/0000-0003-2914-7527/record", curl_params)
       	#Check locked error is returned
        self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

#3.0 tests

    def test_read_private_work_with_30_limited_token(self):
        # Test reading a private work with the 3.0 API and a limited token
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.private_orcid_id + "/work/141943", curl_params)
        self.assertTrue("<error-code>9013</error-code>" in response, "Expected error code 9013 instead: " + response)

    def test_read_private_email_with_30_limited_token(self):
        # Test reading a private email with the 3.0 API and a limited token
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.private_orcid_id + "/email", curl_params)
       	#Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)

    def test_read_deactivated_record_member_api_30(self):
		# Test reading a deactivated record with the member 3.0 API
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/0000-0002-7564-3444/record", curl_params)
        response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2]
       	#Check record has deactivated date
        self.assertTrue(response_body.strip() == open('saved_records/deactivated_record30.xml','r').read(), "No deactivate date " + response_body.strip())

    def test_read_deactivated_record_public_api_30(self):
		# Test reading a deactivated record with the public 3.0 API
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v3.0_rc1/0000-0002-7564-3444/record", curl_params)
        response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2]
       	#Check record has deactivated date
        self.assertTrue(response_body.strip() == open('saved_records/deactivated_record30.xml','r').read(), "No deactivate date " + response_body.strip())

    def test_read_locked_record_member_api_30(self):
		# Test reading a locked record with the member 3.0 API
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/0000-0002-1871-711X/record", curl_params)
       	#Check locked error is returned
        self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_locked_record_public_api_30(self):
		# Test reading a locked record with the public 3.0 API
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v3.0_rc1/0000-0002-1871-711X/record", curl_params)
       	#Check locked error is returned
        self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_deprecated_record_member_api_30(self):
		# Test reading a deprecated record with the member 3.0 API
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/0000-0003-2914-7527/record", curl_params)
       	#Check locked error is returned
        self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

    def test_read_deprecated_record_public_api_30(self):
		# Test reading a deprecated record with the public 3.0 API
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v3.0_rc1/0000-0003-2914-7527/record", curl_params)
       	#Check locked error is returned
        self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)
