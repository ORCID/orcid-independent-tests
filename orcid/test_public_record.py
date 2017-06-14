import OrcidBaseTest
import properties

class PublicRecord(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.public_orcid_id    = '0000-0002-3874-7658'
        self.pubapi_public_token= 'a8ac4d85-df2b-4de2-9411-1b94491f463b'
        self.memapi_public_token= 'eba7892b-4f4a-4651-9c47-f0c74fae61c5'
        self.empty_activities   = '"orcid-activities":null'
        self.empty_bio          = '"orcid-bio":null'
        self.empty_email        = '"email":[]'
        self.activities         = ['educations', 'employments', 'fundings', 'works', 'peer-reviews']
        self.bio_sections2      = ['other-name', 'researcher-url', 'keyword', 'external-identifier', 'email', 'address']
        self.saved_records_path = 'saved_records'

    def test_read_public_record_with_12_public_api(self):
        #TEST 130
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.pubapi_public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v1.2/" + self.public_orcid_id + "/orcid-profile", curl_params)
        response_body = response.partition('</orcid-history>')[2]
        #Compare the body of the response to the saved file.        
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record12.xml','r').read(), 'response_body: ' + response_body)
	
    def test_read_public_record_with_20_public_api(self):
        #TEST 131
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.pubapi_public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/" + self.public_orcid_id + "/record", curl_params)
        response_body = response.partition('</history:history>')[2]
        #Compare the body of the response to the saved file.        
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record20.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_12_member_api(self):
        #TEST 132
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.memapi_public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v1.2/" + self.public_orcid_id + "/orcid-profile", curl_params)
        response_body = response.partition('</orcid-history>')[2]
        #Compare the body of the response to the saved file.        
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record12.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_20_member_api(self):
        #TEST 133
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.memapi_public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.public_orcid_id + "/record", curl_params)
        response_body = response.partition('</history:history>')[2]
        #Compare the body of the response to the saved file.        
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record20.xml','r').read(), 'response_body: ' + response_body)
