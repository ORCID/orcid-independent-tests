import OrcidBaseTest

class PublicApiReadSearch(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        ''' TODO load configuration from java properties file'''
        self.client_id = ""
        self.client_secret = ""
        self.seach_value = "family-name:30sep2016"
        self.orcid_id = "0000-0003-4962-7157"
        self.token = self.orcid_generate_read_public_token(self.client_id, self.client_secret)

    def test_read(self):
        response = self.orcid_curl("https://pub.qa.orcid.org/v2.0_rc4/0000-0001-6085-8875/record", ['-i', '-k', '-H', "Accept: application/xml"])
        self.assertFalse("error-code" in response, "error-code Not found on json response")

    def test_search_my_record(self):
        self.assertIsNotNone(self.token,"No token generated, instead got " + self.token)        
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.token, '-H', 'Accept: application/xml']
        response = self.orcid_curl("https://pub.qa.orcid.org/v1.2/search/orcid-bio/?q=" + self.seach_value, curl_params)
        self.assertTrue("ma_test" in response, "Name not returned on " + response)
        self.assertTrue("ma_public_test" in response,"Public name not returned on " + response)
        
    def test_read_record_with_12_api(self):
        self.assertIsNotNone(self.token,"No token generated, instead got " + self.token)
        '''
        curl -H 'Content-Type: application/xml' -H 'Authorization: Bearer [public token]' -X GET 'http://pub.qa.orcid.org/v1.2/[orcid id]/orcid-profile' -L -i -k
        '''
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("http://pub.qa.orcid.org/v1.2/" + self.orcid_id + "/orcid-profile", curl_params)
        self.assertTrue("ma_test" in response,"Name not returned on " + response)
