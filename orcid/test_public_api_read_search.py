import OrcidBaseTest
import properties
import local_properties


class PublicApiReadSearch(OrcidBaseTest.OrcidBaseTest):
    def setUp(self):
        if properties.type == "jenkins":
            self.test_server = properties.test_server
            self.client_id     = properties.publicClientId
            self.client_secret = properties.publicClientSecret
            self.seach_value   = properties.searchValue
            self.orcid_id      = properties.orcidId
            self.token         = self.orcid_generate_token(self.client_id, self.client_secret)
        else:
            self.test_server = local_properties.test_server
            self.orcid_id = local_properties.orcid_id_member
            self.client_id = local_properties.step_2_client_id
            self.client_secret = local_properties.step_2_client_secret
            self.seach_value = local_properties.searchValue
            self.token = self.orcid_generate_token(self.client_id, self.client_secret)

    def test_read(self):
    # Test read the private record (public without a token) and check no error returned
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.0/0000-0001-6085-8875/record", ['-i', '-k', '-H', "Accept: application/xml"])
        self.assertFalse("error-code" in response, "error-code Not found on json response")

    def test_search_my_record_20(self):
    # Test search for the record with the 2.0 api and check that it is returned
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-H', 'Authorization: Bearer ' + self.token]
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.0/search?q=" + self.seach_value, curl_params)
        self.assertTrue("http://" + self.test_server + "/" + self.orcid_id in response, "Record not returned in search" + response)

    def test_read_record_with_20_api(self):
    # Test read record with the public 2.0 api and check that it is returned
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.0/" + self.orcid_id + "/record", curl_params)
        self.assertTrue("http://" + self.test_server + "/" + self.orcid_id in response, "Name not returned on " + response)

    def test_search_my_record_21(self):
    # Test search for orcid with the 2.1 public api and check it is returned
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-H', 'Authorization: Bearer ' + self.token]
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.1/search?q=" + self.seach_value, curl_params)
        self.assertTrue("https://" + self.test_server + "/" + self.orcid_id in response, "Record not returned in search" + response)

    def test_read_record_with_21_api(self):
    # Test read record with the public 2.1 api and check that it is returned
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.1/" + self.orcid_id + "/record", curl_params)
        self.assertTrue("https://" + self.test_server + "/" + self.orcid_id in response, "Name not returned on " + response)

    def test_search_my_record_30_rc1(self):
    # Test search for orcid with the 3.0_rc1 public api and check it is returned
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-H', 'Authorization: Bearer ' + self.token]
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc1/search?q=" + self.seach_value, curl_params)
        self.assertTrue("https://" + self.test_server + "/" + self.orcid_id in response, "Record not returned in search" + response)

    def test_read_record_with_30_rc1_api(self):
    # Test read record with the public 3.0_rc1 api and check that it is returned
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc1/" + self.orcid_id + "/record", curl_params)
        self.assertTrue("https://" + self.test_server + "/" + self.orcid_id in response, "Name not returned on " + response)

    def test_search_my_record_30_rc2(self):
    # Test search for orcid with the 3.0_rc2 public api and check it is returned
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-H', 'Authorization: Bearer ' + self.token]
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc2/search?q=" + self.seach_value, curl_params)
        self.assertTrue("https://" + self.test_server + "/" + self.orcid_id in response, "Record not returned in search" + response)

    def test_read_record_with_30_rc2_api(self):
    # Test read record with the public 3.0_rc2 api and check that it is returned
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc2/" + self.orcid_id + "/record", curl_params)
        self.assertTrue("https://" + self.test_server + "/" + self.orcid_id in response, "Name not returned on " + response)

    def test_search_my_record_30(self):
    # Test search for orcid with the 3.0 public api and check it is returned
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-H', 'Authorization: Bearer ' + self.token]
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0/search?q=" + self.seach_value, curl_params)
        self.assertTrue("https://" + self.test_server + "/" + self.orcid_id in response, "Record not returned in search" + response)

    def test_read_record_with_30_api(self):
    # Test read record with the public 3.0 api and check that it is returned
        self.assertIsNotNone(self.token,"No token generated")
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0/" + self.orcid_id + "/record", curl_params)
        self.assertTrue("https://" + self.test_server + "/" + self.orcid_id in response, "Name not returned on " + response)
