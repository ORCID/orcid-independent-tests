import OrcidBaseTest
import properties

class PublicRecord(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        p = pyjavaproperties.Properties()
        self.public_orcid_id    = '0000-0002-3874-7658'
        self.limited_token      = 'eba7892b-4f4a-4651-9c47-f0c74fae61c5'
        self.empty_activities   = '"orcid-activities":null'
        self.empty_bio          = '"orcid-bio":null'
        self.empty_email        = '"email":[]'
        self.activities         = ['educations', 'employments', 'fundings', 'works', 'peer-reviews']
        self.bio_sections2      = ['other-name', 'researcher-url', 'keyword', 'external-identifier', 'email', 'address']
        self.saved_records_path = 'saved_records'
        self.client_id     = properties.publicClientId
        self.client_secret = properties.publicClientSecret
        self.scope         = "/authenticate"
        self.read_pub_code = self.generate_auth_code(properties.publicClientId, self.scope,"readPublicCode")        
        self.token         = self.orcid_generate_token(self.client_id, self.client_secret)

    def test_read_public_record_with_12_public_api(self):
        #TEST 130
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v1.2/" + self.public_orcid_id + "/orcid-profile", curl_params)
        response_body = response.partition('X-Frame-Options: DENY')[2]
        #Compare the body of the response to the saved file.        
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record12.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_20_public_api(self):
        #TEST 131
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/" + self.public_orcid_id + "/record", curl_params)
        response_body = response.partition('X-Frame-Options: DENY')[2]
        #Compare the body of the response to the saved file.        
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record20.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_12_member_api(self):
        #TEST 132
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v1.2/" + self.public_orcid_id + "/orcid-profile", curl_params)
        response_body = response.partition('X-Frame-Options: DENY')[2]
        #Compare the body of the response to the saved file.        
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record12.xml','r').read(), 'response_body: ' + response_body)

    def test_read_public_record_with_20_member_api(self):
        #TEST 133
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/" + self.public_orcid_id + "/record", curl_params)
        response_body = response.partition('X-Frame-Options: DENY')[2]
        #Compare the body of the response to the saved file.        
        self.assertTrue(response_body.strip() == open(self.saved_records_path + '/public_record20.xml','r').read(), 'response_body: ' + response_body)
