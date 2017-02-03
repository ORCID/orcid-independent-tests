import OrcidBaseTest
import pyjavaproperties

class ScopeMethods(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test.properties'))
        self.orcid_props   = p
        self.public_client_id     = self.orcid_props['publicClientId']
        self.public_client_secret = self.orcid_props['publicClientSecret']
        self.member_client_id     = self.orcid_props['memberClientId']
        self.member_client_secret = self.orcid_props['memberClientSecret']

    def test_get_read_limited_token(self):
        curl_params = ['-L', '-s', '-D', '-', '-o', '/dev/null']
        response = self.orcid_curl("https://qa.orcid.org/oauth/authorize?client_id=%s&response_type=code&scope=/read-limited&redirect_uri=https://developers.google.com/oauthplayground" % (self.public_client_id), curl_params)
        self.assertTrue("Invalid scope" in response, "Unexpected response: " + response)
        
    def test_get_read_limited_token_via_2stepoauth(self):
        curl_params = ['-i', '-L', '-H', "Accept: application/json", '-d', "client_id=" + self.public_client_id, '-d', "client_secret=" + self.public_client_secret, '-d', "scope=/read-limited", '-d', "grant_type=client_credentials"]
        response = self.orcid_curl("http://pub.qa.orcid.org/oauth/token", curl_params)
        self.assertTrue("401 Unauthorized" in response, "Unexpected response: " + response)