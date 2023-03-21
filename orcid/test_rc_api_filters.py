import OrcidBaseTest
import properties
import local_properties

class RCApiFilters(OrcidBaseTest.OrcidBaseTest):
    def setUp(self):
        # 0000-0002-7361-1027
        if properties.type == "actions":
          self.test_server = properties.test_server
          self.orcid_id = properties.staticId
          self.access = properties.staticAccess
        else:
          self.test_server = local_properties.test_server
          self.orcid_id = local_properties.orcid_id
          self.access = local_properties.step_1_access

    def read(self, endpoint, version):
        curl_params = ['-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
        read_response = self.orcid_curl("https://api." + self.test_server + "/%s/%s/%s" % (version, self.orcid_id, endpoint), curl_params)
        return read_response

    def read_redirect(self, endpoint, version):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
        read_response = self.orcid_curl("https://api." + self.test_server + "/%s/%s/%s" % (version, self.orcid_id, endpoint), curl_params)
        return read_response    

    def assert_20rc_messages(self, read_response):
        self.assertTrue("HTTP/1.1 308" in read_response and "HTTP/1.1 200" not in read_response, "response: " + read_response)
        self.assertTrue("<response-code>308</response-code>" in read_response, "response: " + read_response)
        self.assertTrue("<developer-message>Release candidates for V2.0 are now disabled, your request will be redirected to the corresponding V2.0 end point</developer-message>" in read_response, "response: " + read_response)
        self.assertTrue("<user-message>Release candidates for V2.0 are now disabled, your request will be redirected to the corresponding V2.0 end point</user-message>" in read_response, "response: " + read_response)
        self.assertTrue("<error-code>9056</error-code>" in read_response, "response: " + read_response)

    def assert_30rc_messages(self, read_response):
        self.assertTrue("HTTP/1.1 308" in read_response and "HTTP/1.1 200" not in read_response, "response: " + read_response)
        self.assertTrue("<response-code>308</response-code>" in read_response, "response: " + read_response)
        self.assertTrue("<developer-message>Release candidates for V3.0 are now disabled, your request will be redirected to the corresponding V3.0 end point</developer-message>" in read_response, "response: " + read_response)
        self.assertTrue("<user-message>Release candidates for V3.0 are now disabled, your request will be redirected to the corresponding V3.0 end point</user-message>" in read_response, "response: " + read_response)
        self.assertTrue("<error-code>9056</error-code>" in read_response, "response: " + read_response)

    def assert_redirection(self, read_response):
        self.assertTrue("HTTP/1.1 308" in read_response and "HTTP/1.1 200" in read_response, "response: " + read_response)

    def test_works30_rc1(self):
        read_response = self.read_redirect('works', "v3.0_rc1")
        self.assertTrue("HTTP/1.1 308" in read_response and "HTTP/1.1 200" in read_response, "response: " + read_response)
        read_response = self.read('works', "v3.0_rc1")
        self.assert_30rc_messages(read_response) 

    def test_works30_rc2(self):
        read_response = self.read_redirect('works', "v3.0_rc2")
        self.assertTrue("HTTP/1.1 308" in read_response and "HTTP/1.1 200" in read_response, "response: " + read_response)
        read_response = self.read('works', "v3.0_rc2")
        self.assert_30rc_messages(read_response) 

    def test_works20_rc1(self):
        read_response = self.read_redirect('works', "v2.0_rc1")
        self.assertTrue("HTTP/1.1 308" in read_response and "HTTP/1.1 200" in read_response, "response: " + read_response)
        read_response = self.read('works', "v2.0_rc1")
        self.assert_20rc_messages(read_response)      

    def test_works20_rc2(self):
        read_response = self.read_redirect('works', "v2.0_rc2")
        self.assertTrue("HTTP/1.1 308" in read_response and "HTTP/1.1 200" in read_response, "response: " + read_response)
        read_response = self.read('works', "v2.0_rc2")
        self.assert_20rc_messages(read_response) 

    def test_works20_rc3(self):
        read_response = self.read_redirect('works', "v2.0_rc3")
        self.assertTrue("HTTP/1.1 308" in read_response and "HTTP/1.1 200" in read_response, "response: " + read_response)
        read_response = self.read('works', "v2.0_rc3")
        self.assert_20rc_messages(read_response) 

    def test_works20_rc4(self):
        read_response = self.read_redirect('works', "v2.0_rc4")
        self.assertTrue("HTTP/1.1 308" in read_response and "HTTP/1.1 200" in read_response, "response: " + read_response)
        read_response = self.read('works', "v2.0_rc4")
        self.assert_20rc_messages(read_response) 