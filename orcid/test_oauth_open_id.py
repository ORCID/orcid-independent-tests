import OrcidBaseTest
import OrcidBrowser
import properties

class OauthOpenId(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.client_id     = properties.publicClientId
        self.browser       = OrcidBrowser.OrcidBrowser
        self.usrname       = ""
        self.secret        = ""

    def test_grant_with_implicit_request(self):
        self.browser.getToken(self.usrname, self.secret, self.client_id)
        self.assertTrue("-" in response, "we got an implicit token: " + response)

    def test_generate_read_limited(self):
        self.assertTrue(1)

    def test_not_exchanged_expires(self):
        self.assertTrue(1)

    def test_call_user_info(self):
        self.assertTrue(1)

    def test_generate_exchange(self):
        self.assertTrue(1)

    def test_generate_revoke(self):
        self.assertTrue(1)

    def test_generate_auth_code_with_openid_scope(self):
        self.assertTrue(1)

    def test_all_endpoints(self):
        self.assertTrue(1)






