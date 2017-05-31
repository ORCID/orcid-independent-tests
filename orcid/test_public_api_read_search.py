import OrcidBaseTest
import properties

class PublicApiReadSearch(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.client_id     = properties.publicClientId
        self.client_secret = properties.publicClientSecret
        self.seach_value   = properties.searchValue
        self.orcid_id      = properties.orcidId
        self.scope         = "/authenticate"
        self.read_pub_code = self.generate_auth_code(properties.publicClientId, self.scope,"readPublicCode")
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.read_pub_code)
        self.token         = self.orcid_generate_token(self.client_id, self.client_secret)

    def test_read(self):
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0_rc4/0000-0001-6085-8875/record", ['-i', '-k', '-H', "Accept: application/xml"])
        self.assertFalse("error-code" in response, "error-code Not found on json response")

    def test_search_my_record(self):
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-H', 'Authorization: Bearer ' + self.token]
        response = self.orcid_curl("http://pub." + properties.test_server + "/v1.2/search/orcid-bio/?q=" + self.seach_value, curl_params)
        self.assertTrue("ma_test" in response, "Name " + self.seach_value + " not returned on " + response)
        #self.assertTrue("ma_public_test" in response, "Public name not returned on " + response)

    def test_read_record_with_12_api(self):
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("http://pub." + properties.test_server + "/v1.2/" + self.orcid_id + "/orcid-profile", curl_params)
        self.assertTrue("ma_test" in response, "Name not returned on " + response)

    def test_read_record_with_20_api(self):
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0_rc3/" + self.orcid_id + "/record", curl_params)
        self.assertTrue("ma_test" in response, "Name not returned on " + response)

    def test_read_record_without_access_token(self):
        curl_params = ['-H', "Accept: application/xml", '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("http://pub." + properties.test_server + "/v1.2/" + self.orcid_id + "/orcid-profile", curl_params)
        self.assertTrue("ma_test" in response, "Data returned without requiring token " + response)
