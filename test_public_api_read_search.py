import OrcidBaseTest

class PublicApiReadSearch(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        ''' TODO load configuration from java properties file'''
        self.client_id = ""
        self.client_secret = ""
        self.seach_value = "family-name:ma_22112016"

    def test_read(self):
        response = self.orcid_curl("https://pub.qa.orcid.org/v2.0_rc4/0000-0001-6085-8875/record", ['-i', '-k', '-H', "Accept: application/xml"])
        self.assertFalse("error-code" in response, "error-code Not found on json response")

    def test_search_my_record(self):
        token = self.orcid_generate_read_public_token(self.client_id, self.client_secret)
        self.assertIsNotNone(token,"No token generated, instead got " + token)
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + token, '-H', 'Accept: application/xml']
        response = self.orcid_curl("https://pub.qa.orcid.org/v1.2/search/orcid-bio/?q=" + self.seach_value, curl_params)
        self.assertTrue("ma_test" in response,"Public name not returned on " + response)
        