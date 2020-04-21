import OrcidBaseTest
import properties
import local_properties

class ScopeMethods(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        if local_properties.type == "jenkins":
            self.test_server = properties.test_server
            self.public_client_id     = properties.publicClientId
            self.public_client_secret = properties.publicClientSecret
            self.member_client_id     = properties.premiumClientId
            self.member_client_secret = properties.premiumClientSecret
        else:
            self.test_server = local_properties.test_server
            self.public_client_id = local_properties.publicClientId
            self.public_client_secret = local_properties.publicClientSecret
            self.member_client_id = local_properties.premiumClientId
            self.member_client_secret = local_properties.premiumClientSecret

    def test_get_read_limited_token_with_basic(self):
        #Test you can't get a /read-limited token with a public client
        curl_params = ['-L', '-s', '-D', '-', '-o', '/dev/null']
        response = self.orcid_curl("https://" + self.test_server + "/oauth/authorize?client_id=%s&response_type=code&scope=/read-limited&redirect_uri=https://developers.google.com/oauthplayground" % (self.public_client_id), curl_params)
        self.assertTrue("Invalid scope" in response, "Unexpected response: " + response)

    def test_get_read_limited_token_via_2stepoauth(self):
        #Test you can't get a read-limited token with 2step OAuth
        curl_params = ['-i', '-L', '-k', '-H', "Accept: application/json", '-d', "client_id=" + self.public_client_id, '-d', "client_secret=" + self.public_client_secret, '-d', "scope=/read-limited", '-d', "grant_type=client_credentials"]
        response = self.orcid_curl("https://" + self.test_server + "/oauth/token", curl_params)
        self.assertTrue("400" in response, "Unexpected response (/read-limited): " + response)

    def test_get_read_webhook_with_basic_client(self):
        #Test you can't get webhook token with a basic client
        curl_params = ['-i', '-L', '-k', '-H', "Accept: application/json", '-d', "client_id=" + self.member_client_id, '-d', "client_secret=" + self.member_client_secret, '-d', "scope=/web-hook", '-d', "grant_type=client_credentials"]
        response = self.orcid_curl("https://" + self.test_server + "/oauth/token", curl_params)
        self.assertTrue("400" in response, "Unexpected response(/web-hook): " + response)

    def test_get_profile_create(self):
        #Test orcid-profile/create scope does not work
        curl_params = ['-i', '-L', '-k', '-H', "Accept: application/json", '-d', "client_id=" + self.member_client_id, '-d', "client_secret=" + self.member_client_secret, '-d', "scope=/orcid-profile/create", '-d', "grant_type=client_credentials"]
        response = self.orcid_curl("https://" + self.test_server + "/oauth/token", curl_params)
        self.assertTrue("400" in response, "Unexpected response (/orcid-profile/create): " + response)
        
    def test_2step_pub_endpoint(self):
        #Test you can get a 2 step token using the public API endpoint
        curl_params = ['-i', '-L', '-k', '-H', "Accept: application/json", '-d', "client_id=" + self.public_client_id, '-d', "client_secret=" + self.public_client_secret, '-d', "scope=/read-public", '-d', "grant_type=client_credentials"]
        response = self.orcid_curl("https://pub." + self.test_server + "/oauth/token", curl_params)
        self.assertTrue("access_token" in response, "Unexpected response: " + response)
        
    def test_2step_member_endpoint(self):
        #Test you can get a 2 step token using the public API endpoint
        curl_params = ['-i', '-L', '-k', '-H', "Accept: application/json", '-d', "client_id=" + self.member_client_id, '-d', "client_secret=" + self.member_client_secret, '-d', "scope=/read-public", '-d', "grant_type=client_credentials"]
        response = self.orcid_curl("https://api." + self.test_server + "/oauth/token", curl_params)
        self.assertTrue("access_token" in response, "Unexpected response: " + response)
