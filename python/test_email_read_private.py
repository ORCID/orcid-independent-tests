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
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)

    def test_blank(self):
        curl_params = ['-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma_work.xml', '-X', 'POST']
        response = self.orcid_curl("", curl_params)
        self.assertTrue(True)


