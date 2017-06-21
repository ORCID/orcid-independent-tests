import OrcidBaseTest
import properties

class Refresh(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.client_id     = properties.memberClientId
        self.client_secret = properties.memberClientSecret
        self.orcid_id      = properties.orcidId
        self.scope               = "/read-limited%20/activities/update"
        self.code                = self.generate_auth_code(self.client_id, self.scope, "refresh_tokens")
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id, self.client_secret, self.code)

    def test_1refresh_like_for_like(self):
        #Generate a new access_token
        self.token1 = self.orcid_refresh_token(self.client_id, self.client_secret, self.access, self.refresh)
        #check new token works
        response = self.read_record(self.token1)
        self.assertTrue("<common:path>%s</common:path>" % self.orcid_id in response, "Refresh token read response: " + response)
        #check old token still works
        response = self.read_record(self.access)
        self.assertTrue("<common:path>%s</common:path>" % self.orcid_id in response, "Original access token read response: " + response)

    def test_2refresh_subset(self):
        #Generate a new token with just the read-limit scope and revoke the old token
        self.token2 = self.orcid_refresh_token(self.client_id, self.client_secret, self.access, self.refresh, "/read-limited", "true")
        #Check the new token can't post a work
        response = self.post_activity_refresh(self.token2)
        self.assertTrue("<error-code>9038</error-code>" in response, "Post with read refresh token response: " +response)
        #Check the revoked token can't read the record
        response = self.read_record(self.access)
        self.assertTrue("invalid_token" in response, "Read with revoked token response: " + response)

    def test_3refresh_disabled(self):
        #Test that a disabled token can't be used to generate a refresh token
        self.disabled = self.orcid_refresh_token(self.client_id, self.client_secret, self.access, self.refresh)
        self.assertTrue("Parent token is disabled" in str(self.disabled), "Expected token disabled error instead " + str(self.disabled))
        
