import OrcidBaseTest
import pyjavaproperties

class Webhook(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test-client.properties'))
        self.orcid_props   = p
        self.client_id     = self.orcid_props['memberClientId']
        self.client_secret = self.orcid_props['memberClientSecret']
        self.orcid_id      = self.orcid_props['orcidId']
        self.token         = self.orcid_generate_member_token(self.client_id, self.client_secret, 'webhook')

    def test_webhook(self):
        self.assertIsNotNone(self.token,"No token generated, instead got " + self.token)
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.token, '-L', '-i', '-k', '-X', 'PUT']
        response = self.orcid_curl("http://api.qa.orcid.org/" + self.orcid_id + "/webhook/http%3A%2F%2Fnowhere2.com%2Fupdated", curl_params)
        self.assertTrue("201 Created" in response, "Unexpected response: " + response)