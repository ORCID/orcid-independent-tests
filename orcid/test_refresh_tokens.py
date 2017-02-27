import OrcidBaseTest
import pyjavaproperties

class RefreshTokens(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test.properties'))
        self.orcid_props           = p
        self.client_id             = self.orcid_props['memberClientId']
        self.client_secret         = self.orcid_props['memberClientSecret']
        self.orcid_id              = self.orcid_props['orcidId']
        self.code2                 = self.orcid_props['api2PostUpdateCode']
        self.access2,self.refresh2 = self.orcid_exchange_auth_token(self.client_id, self.client_secret, self.code2)        
        
    def test_access_wrong_record1(self):
        # curl -i -L -k -H 'Authorization: Bearer 7b5557d8-add6-4c39-b55d-2e7dae643998' -d 'refresh_token=b3f63880-3506-43e4-b319-ca32a44bf378' -d 'grant_type=refresh_token' -d 'client_id=APP-AJPEHIAZIRSSY5UO' -d 'client_secret=580f5b9c-59b4-4408-9228-7be97d0f8000' -d 'revoke_old=false' https://qa.orcid.org/oauth/token
        # TEST 118
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access2, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@', '-d', '']
        response = self.orcid_curl("http://api.qa.orcid.org/v1.2/" + self.wrong_orcid_id + "/orcid-works", curl_params)
        self.assertTrue("403 Forbidden" in response, "response: " + response)