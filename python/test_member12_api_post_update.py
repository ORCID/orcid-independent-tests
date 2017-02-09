import OrcidBaseTest
import pyjavaproperties

class Member12ApiReadDelete(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test.properties'))
        self.orcid_props   = p
        self.client_id     = self.orcid_props['memberClientId']
        self.client_secret = self.orcid_props['memberClientSecret']        
        self.code          = self.orcid_props['api1PostUpdateCode']
        self.orcid_id      = self.orcid_props['orcidId']
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)

    def test_post_work(self):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.webhook_access, '-H', 'Content-Length: 0', '-H', 'Accept: application/json', '-k', '-X', 'PUT']
        response = self.orcid_curl("http://api.qa.orcid.org/%s/webhook/%s" % (self.orcid_id, "http%3A%2F%2Fnowhere.net%2Fupdated"), curl_params)
        self.assertTrue("201 Created" in response, "response: " + response)
