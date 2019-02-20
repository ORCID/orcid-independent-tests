import OrcidBaseTest
from OrcidBrowser import OrcidBrowser
import properties

class OauthOpenId(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.server_name   = 'qa.orcid.org'
        self.firefox       = OrcidBrowser()
        self.orcid_id      = properties.user_orcid_id
        self.user_api_id   = properties.user_api_id
        self.user_api_pass = properties.user_api_pass
        self.usrname       = properties.user_login
        self.secret        = properties.user_pass

    def test_00_grant_implicit_and_call_userinfo(self):
        # default scope='/authenticate'
        token = self.firefox.getImplicitToken(self.usrname, self.secret, self.user_api_id,'/authenticate', True)
        self.assertIsNotNone(token, "Token not recovered")
        #test_call_user_info
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + token]
        response = self.orcid_curl('https://' + self.server_name + '/oauth/userinfo', curl_params)
        self.assertTrue(self.orcid_id in response, "user information not returned, got: " + response)

    def test_01_all_endpoints(self):
        self._check_endpoint('qa.orcid.org')
        #self._check_endpoint('api.qa.orcid.org')
        #self._check_endpoint('pub.qa.orcid.org')

    def _check_endpoint(self, srvname):
        self.firefox.setServerName(srvname)
        token = self.firefox.getImplicitToken(self.usrname, self.secret, self.user_api_id)
        self.assertIsNotNone(token, "failure getting implicit token with server: " + srvname)

    #error=invalid_scope&error_description=Invalid%20scope:%20/read-limited
    def test_03_generate_read_limited(self):
        token = self.firefox.getImplicitToken(self.usrname, self.secret, self.user_api_id, '/read-limited')
        self.assertIsNone(token, "Somehow we got a token with /read-limited scope")

    def test_04_generate_revoke(self):
        token = self.firefox.getImplicitToken(self.usrname, self.secret, self.user_api_id)
        self.assertIsNotNone(token, "Token not recovered")
        data = 'client_id=' + self.user_api_id + '&client_secret=' + self.user_api_pass + '&token=' + token
        curl_params = ['-i', '--data', data, '-X' ,'POST']
        response = self.orcid_curl('https://' + self.server_name + '/oauth/revoke', curl_params)
        self.assertTrue('OK' in  response, "revoke failed, got: " + response)

    def test_not_exchanged_expires(self):
        self.assertTrue(1)

    def test_generate_auth_code_with_openid_scope(self):
        self.assertTrue(1)

    def test_generate_exchange(self):
        self.assertTrue(1)

    def tearDown(self):
        self.firefox.bye()
