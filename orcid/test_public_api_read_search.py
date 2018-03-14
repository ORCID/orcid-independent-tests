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
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/0000-0001-6085-8875/record", ['-i', '-k', '-H', "Accept: application/xml"])
        self.assertFalse("error-code" in response, "error-code Not found on json response")
        
    def test_search_my_record_20(self):
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-H', 'Authorization: Bearer ' + self.token]
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/search?q=" + self.seach_value, curl_params)
        self.assertTrue("http://" + properties.test_server + "/" + self.orcid_id in response, "Record not retuned in search" + response)

    def test_read_record_with_20_api(self):
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/" + self.orcid_id + "/record", curl_params)
        self.assertTrue("http://" + properties.test_server + "/" + self.orcid_id in response, "Name not returned on " + response)
        
    def test_search_my_record_21(self):
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-H', 'Authorization: Bearer ' + self.token]
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.1/search?q=" + self.seach_value, curl_params)
        self.assertTrue("https://" + properties.test_server + "/" + self.orcid_id in response, "Record not retuned in search" + response)

    def test_read_record_with_21_api(self):
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + properties.test_server + "/v2.1/" + self.orcid_id + "/record", curl_params)
        self.assertTrue("https://" + properties.test_server + "/" + self.orcid_id in response, "Name not returned on " + response)

