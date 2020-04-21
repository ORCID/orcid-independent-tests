import OrcidBaseTest
from OrcidBrowser import OrcidBrowser
import properties
import local_properties

class OauthOpenId(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.scope = "openid"
        self.wrong_scope = "/read-limited%20/activities/update%20/person/update"
        if local_properties.type == "jenkins":
          self.test_server = properties.test_server
          self.public_record_id    = properties.staticId
          self.public_record_token = "c9974dc3-451b-420f-ae6e-b76d7009062e"
          self.limited_record_token = "2fe47c3c-aae6-4a80-981b-fc221a067abe"
          self.client_id = properties.OpenClientId
          self.client_secret = properties.OpenClientSecret
        else:
          self.test_server = local_properties.test_server
          self.public_record_id = local_properties.orcid_id_member
          self.public_record_token = "c9974dc3-451b-420f-ae6e-b76d7009062e"
          self.limited_record_token = "2fe47c3c-aae6-4a80-981b-fc221a067abe"
          self.client_id = local_properties.OpenClientId
          self.client_secret = local_properties.OpenClientSecret

    def get_user_info(self, token):
        self.assertIsNotNone(token,"Bearer not recovered: " + str(token))
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(token)]
        response = self.orcid_curl("https://" + self.test_server + "/oauth/userinfo", curl_params)
        return response

    def test_oauth_token(self):
        code = self.generate_auth_code(self.client_id, self.scope, "open")
        access, refresh, id_token = self.orcid_exchange_auth_token(self.client_id, self.client_secret, code)
        self.assertTrue(access, "Failed to retrieve access token")

    def test_public_record_info(self):
        user_info = self.get_user_info(self.public_record_token)
        user_info_body = user_info.partition('{"id')[1] + user_info.partition('{"id')[2]
        print "response: " + user_info_body
        self.assertTrue(user_info_body.strip() == open('saved_records/user_info_public.json', 'r').read(),'User info does not match saved file: ' + user_info)

    def test_limited_record_info(self):
        user_info = self.get_user_info(self.limited_record_token)
        user_info_body = user_info.partition('{"id')[1] + user_info.partition('{"id')[2]
        print "response: " + user_info_body
        self.assertTrue(user_info_body.strip() == open('saved_records/user_info_limited.json', 'r').read(),'User info does not match saved file: ' + user_info)

    def test_implicit_token(self):
        implicit = self.generate_implicit_code_selenium(self.client_id, self.scope, "open")
        print "implicit: " + implicit
        self.assertTrue(implicit, "Failed to retrieve implicit token")

    def test_wrong_scope_token(self):
        wrong_implicit = self.generate_implicit_code_selenium(self.client_id, self.wrong_scope, "open")
        print "wrong_implicit: " + wrong_implicit
        user_info = self.get_user_info(wrong_implicit)
        print "user_info: " + user_info
        self.assertTrue("access_denied" in user_info, "Wrong scope test failed: " + user_info)
