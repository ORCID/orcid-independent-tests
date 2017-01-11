import OrcidBaseTest
import pyjavaproperties

class PublicApiReadSearch(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test-client.properties'))
        self.orcid_props   = p
        self.client_id     = self.orcid_props['clientId']
        self.client_secret = self.orcid_props['clientSecret']
        self.seach_value   = "family-name:" + self.orcid_props['searchValue']
        self.orcid_id      = self.orcid_props['orcidId']
        self.token         = self.orcid_generate_read_public_token(self.client_id, self.client_secret)

    def test_read(self):
        response = self.orcid_curl("https://pub.qa.orcid.org/v2.0_rc4/0000-0001-6085-8875/record", ['-i', '-k', '-H', "Accept: application/xml"])
        self.assertFalse("error-code" in response, "error-code Not found on json response")

    def test_search_my_record(self):
        self.assertIsNotNone(self.token,"No token generated, instead got " + self.token)        
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.token, '-H', 'Accept: application/xml']
        response = self.orcid_curl("https://pub.qa.orcid.org/v1.2/search/orcid-bio/?q=" + self.seach_value, curl_params)
        self.assertTrue("ma_test" in response, "Name not returned on " + response)
        self.assertTrue("ma_public_test" in response, "Public name not returned on " + response)

    def test_read_record_with_12_api(self):
        self.assertIsNotNone(self.token,"No token generated, instead got " + self.token)
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("http://pub.qa.orcid.org/v1.2/" + self.orcid_id + "/orcid-profile", curl_params)
        self.assertTrue("ma_test" in response, "Name not returned on " + response)

    def test_read_record_with_20_api(self):
        self.assertIsNotNone(self.token,"No token generated, instead got " + self.token)
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("http://pub.qa.orcid.org/v2.0_rc3/" + self.orcid_id + "/orcid-profile", curl_params)
        self.assertTrue("ma_test" in response, "Name not returned on " + response)

    def test_read_record_without_access_token(self):
        curl_params = ['-H', "Accept: application/xml", '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("http://pub.qa.orcid.org/v1.2/" + self.orcid_id + "/orcid-profile", curl_params)
        self.assertFalse("ma_test" in response, "Data returned withour requiring token" + response)
