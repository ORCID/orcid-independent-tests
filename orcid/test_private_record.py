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

    def test_read_private_record_with_12_public_api(self):
    	#TEST 165
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v1.2/" + self.private_orcid_id + "/orcid-profile", curl_params)
		#Check the name and email address are not returned anywhere        
        self.assertFalse('Published Name' in response, "Name returned " + response)
        self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
		#Check an empty bio and activities sections are returned
        self.assertTrue(self.empty_activities in response, "Non-empty activities returned " + response)
        self.assertTrue(self.empty_bio in response, "Non-empty bio returned " + response) 
        
    def test_read_private_record_with_20_public_api(self):
    	#TEST 165
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
	        
    def test_read_private_record_with_12_limited_token(self):
    	#TEST 167
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
    	#TEST 168
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
	        
    def test_read_private_work_with_20_limited_token(self):
        # TEST 169
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.private_orcid_id + "/work/141943", curl_params)
        self.assertTrue("<error-code>9013</error-code>" in response, "Expected error code 9013 instead: " + response) 
    
    def test_read_private_email_with_20_limited_token(self):
        # TEST 171
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.private_orcid_id + "/email", curl_params)
       	#Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email retruned " + response)  
        
        
