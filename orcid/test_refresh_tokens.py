import OrcidBaseTest
import properties

class RefreshTokens(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.client_id             = properties.memberClientId
        self.client_secret         = properties.memberClientSecret
        self.orcid_id              = properties.orcidId
        self.scope               = "/orcid-bio/update%20/orcid-works/create%20/orcid-works/update%20/affiliations/create%20/affiliations/update%20/funding/create%20/funding/update%20/orcid-profile/read-limited"
        self.code                = self.generate_auth_code(self.client_id,self.scope, "api2PostUpdateCode")
        self.access2,self.refresh2 = self.orcid_exchange_auth_token(self.client_id, self.client_secret, self.code)        
        
    def test_access_wrong_record1(self):
        # curl -i -L -k -H 'Authorization: Bearer 7b5557d8-add6-4c39-b55d-2e7dae643998' -d 'refresh_token=b3f63880-3506-43e4-b319-ca32a44bf378' -d 'grant_type=refresh_token' -d 'client_id=APP-AJPEHIAZIRSSY5UO' -d 'client_secret=580f5b9c-59b4-4408-9228-7be97d0f8000' -d 'revoke_old=false' https://qa.orcid.org/oauth/token
        # TEST 118
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access2, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@', '-d', '']
        response = self.orcid_curl("http://api." + properties.test_server + "/v1.2/" + self.wrong_orcid_id + "/orcid-works", curl_params)
        self.assertTrue("403 Forbidden" in response, "response: " + response)