import OrcidBaseTest
from OrcidBrowser import OrcidBrowser
import properties

class OauthOpenId(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.firefox = OrcidBrowser()
        self.client_id = "APP-52PDPI669AHFVT3V"
        self.scope = "openid"
        self.client_secret = "8e242970-5d2a-4b47-b7d3-c88165a10bfb"
        self.code = self.generate_auth_code(self.client_id, self.scope, "open")
        self.access, self.refresh = self.orcid_exchange_auth_token(self.client_id, self.client_secret, self.code)

    def test_aaa(self):


        print self.code
        print " "
        print self.access
        self.assertTrue(1==2, "code: " + self.code + ", access = " + self.access)
