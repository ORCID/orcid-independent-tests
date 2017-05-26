import OrcidBaseTest
import properties

class ScopeMethods(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.public_client_id     = properties.publicClientId
        self.public_client_secret = properties.publicClientSecret
        self.member_client_id     = properties.premiumClientId
        self.member_client_secret = properties.premiumClientSecret

    def test_get_read_limited_token(self):
        """ TEST 172 """
        curl_params = ['-L', '-s', '-D', '-', '-o', '/dev/null']
        response = self.orcid_curl("https://" + properties.test_server + "/oauth/authorize?client_id=%s&response_type=code&scope=/read-limited&redirect_uri=https://developers.google.com/oauthplayground" % (self.public_client_id), curl_params)
        self.assertTrue("Invalid scope" in response, "Unexpected response: " + response)
        
    def test_get_read_limited_token_via_2stepoauth(self):
        """ TEST 173 """
        curl_params = ['-i', '-L', '-k', '-H', "Accept: application/json", '-d', "client_id=" + self.public_client_id, '-d', "client_secret=" + self.public_client_secret, '-d', "scope=/read-limited", '-d', "grant_type=client_credentials"]
        response = self.orcid_curl("http://pub." + properties.test_server + "/oauth/token", curl_params)
        self.assertTrue("400" in response, "Unexpected response (/read-limited): " + response)
        
    def test_get_activities_update_with_non_institution_client(self):
        """ TEST 174 """
        curl_params = ['-i', '-L', '-k', '-H', "Accept: application/json", '-d', "client_id=" + self.member_client_id, '-d', "client_secret=" + self.member_client_secret, '-d', "scope=/activities/update", '-d', "grant_type=client_credentials"]
        response = self.orcid_curl("http://pub." + properties.test_server + "/oauth/token", curl_params)
        self.assertTrue("400" in response, "Unexpected response(/activities/update): " + response)
        
    def test_get_read_webhook_with_non_institution_client(self):
        """ TEST 175 """
        curl_params = ['-i', '-L', '-k', '-H', "Accept: application/json", '-d', "client_id=" + self.member_client_id, '-d', "client_secret=" + self.member_client_secret, '-d', "scope=/web-hook", '-d', "grant_type=client_credentials"]
        response = self.orcid_curl("http://pub." + properties.test_server + "/oauth/token", curl_params)
        self.assertTrue("400" in response, "Unexpected response(/web-hook): " + response)
        
    def test_get_profile_create_with_non_institution_client(self):
        """ TEST 176 """
        curl_params = ['-i', '-L', '-k', '-H', "Accept: application/json", '-d', "client_id=" + self.member_client_id, '-d', "client_secret=" + self.member_client_secret, '-d', "scope=/orcid-profile/create", '-d', "grant_type=client_credentials"]
        response = self.orcid_curl("http://pub." + properties.test_server + "/oauth/token", curl_params)
        self.assertTrue("400" in response, "Unexpected response (/orcid-profile/create): " + response)