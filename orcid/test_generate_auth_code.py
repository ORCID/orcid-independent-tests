import OrcidBaseTest
from OrcidBrowser import OrcidBrowser
import properties

class GenerateAuthCode(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.firefox       = OrcidBrowser()
        self.user_login    = properties.user_login
        self.user_pass     = properties.user_pass
        self.public_client_id = properties.publicClientId

    def test_create_auth_code_with_scope(self):
        code = self.firefox.getAuthCode(self.user_login,self.user_pass,self.public_client_id)
        self.assertIsNotNone(code, "oauth code returned is None")

    def tearDown(self):
        self.firefox.bye()
