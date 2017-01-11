import OrcidBaseTest
import pyjavaproperties

class MemberApiPostUpdate(OrcidBaseTest.OrcidBaseTest):
    
    xml_data_files_path = '../ORCID-Source/orcid-integration-test/src/test/manual-test/'

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test-client.properties'))
        self.orcid_props   = p
        self.client_id     = self.orcid_props['memberClientId']
        self.client_secret = self.orcid_props['memberClientSecret']        
        self.code          = self.orcid_props['memberCode']
        self.orcid_id      = self.orcid_props['orcidId']

    def test_post_work(self):
        access,refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma_work.xml', '-X', 'POST']
        response = self.orcid_curl("http://api.qa.orcid.org/v1.2/%s/orcid-works" % self.orcid_id, curl_params)
        self.assertTrue(False, "response: " + response)
