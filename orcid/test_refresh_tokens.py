import OrcidBaseTest
import properties

class Refresh(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.client_id     = properties.memberClientId
        self.client_secret = properties.memberClientSecret
        self.notify_token  = properties.notifyToken
        self.orcid_id      = properties.orcidId
        self.scope               = "/read-limited%20/activities/update"
        self.code                = self.generate_auth_code(self.client_id, self.scope, "refresh_tokens")
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)

def test_refresh_like_for_like(self):
    #Generate a new access_token
    self.token1 = self.orcid_refresh_token(self.client_id, self.client_secret, self.access, self.refresh)
    response = self.read_record(self.token1)
    self.assertTrue("<common:path>%s</common:path>" % self.orcid_id in response, "Refresh token read response: " + response)
