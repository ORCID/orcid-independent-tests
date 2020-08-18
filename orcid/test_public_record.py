import OrcidBaseTest
import properties
import re
import local_properties

class PublicRecord(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        if local_properties.type == "jenkins":
          self.test_server = properties.test_server
        else:
          self.test_server = local_properties.test_server
        self.public_orcid_id    = '0000-0002-3874-7658'
        self.pubapi_public_token= 'a8ac4d85-df2b-4de2-9411-1b94491f463b'
        self.memapi_public_token= 'eba7892b-4f4a-4651-9c47-f0c74fae61c5'
        self.empty_activities   = '"orcid-activities":null'
        self.empty_bio          = '"orcid-bio":null'
        self.empty_email        = '"email":[]'
        self.activities         = ['educations', 'employments', 'fundings', 'works', 'peer-reviews']
        self.bio_sections2      = ['other-name', 'researcher-url', 'keyword', 'external-identifier', 'email', 'address']
        self.saved_records_path = 'saved_records'

    def getResponse(self, response):
       return re.sub('[    ](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\n','', response)
    
    def test_read_public_record_with_20_public_api(self):
        #Read the record with the public API with 2.0
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.pubapi_public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/" + self.public_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record20.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_21_public_api(self):
        #Read the record with the public API with 2.1
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.pubapi_public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.1/" + self.public_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record21.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_20_member_api(self):
        #Read the record with the member API with 2.0
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.memapi_public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.public_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record20.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_21_member_api(self):
        #Read the record with the member API with 2.1
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.memapi_public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.1/" + self.public_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record21.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_30rc1_public_api(self):
        #Read the record with the public API with 3.0_rc1
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.pubapi_public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v3.0_rc1/" + self.public_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record30.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_30rc1_member_api(self):
        #Read the record with the member API with 3.0_rc1
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.memapi_public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc1/" + self.public_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record30.xml','r').read(), 'response_body: ' + response_body)
    
    def test_read_public_record_with_30rc2_public_api(self):
        #Read the record with the public API with 3.0_rc2
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.pubapi_public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v3.0_rc2/" + self.public_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record30.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_30rc2_member_api(self):
        #Read the record with the member API with 3.0_rc2
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.memapi_public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0_rc2/" + self.public_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record30.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_30_public_api(self):
        #Read the record with the public API with 3.0
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.pubapi_public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v3.0/" + self.public_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record30.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_30_member_api(self):
        #Read the record with the member API with 3.0
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.memapi_public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v3.0/" + self.public_orcid_id + "/record", curl_params)
        response_body = self.getResponse(response)
        #Compare the body of the response to the saved file.
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record30.xml','r').read(), 'response_body: ' + response_body)

    def test_public_last_modified(self):
    	#Check the last modified date on the record has not changed
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.memapi_public_token, '-L', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.public_orcid_id + "/record", curl_params)
        #Check the record has not been modified since Aug 14th 2017
        self.assertTrue('submission-date":{"value":1457029566956},"last-modified-date":{"value":1528904017670}' in response, "Last modified date has changed" + response)
