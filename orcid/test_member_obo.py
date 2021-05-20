import OrcidBaseTest
from OrcidBrowser import OrcidBrowser
import properties
import json
import re
import local_properties

class OauthOpenId(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
       # self.obo_token = ""
        self.version = "/v3.0/"
        self.first_obo_scope = "openid"
        if properties.type == "jenkins":
            self.test_server = properties.test_server
            self.orcid_id = properties.orcidId
            self.first_obo_id = properties.OBOMemberClientId
            self.first_obo_secret = properties.OBOMemberClientSecret
            self.second_obo_id     = properties.OBOMemberSecondId
            self.second_obo_secret = properties.OBOMemberSecondSecret
        else:
            self.test_server = local_properties.test_server
            self.orcid_id = local_properties.orcid_id_member
            self.first_obo_id = local_properties.OBOMemberClientId
            self.first_obo_secret = local_properties.OBOMemberClientSecret
            self.second_obo_id = local_properties.OBOMemberSecondId
            self.second_obo_secret = local_properties.OBOMemberSecondSecret

        self.first_obo_code = self.generate_auth_code(self.first_obo_id, self.first_obo_scope, "api2PostUpdateCode")
        self.first_obo_access, self.first_obo_refresh, self.first_obo_id_token = self.orcid_exchange_auth_token(self.first_obo_id, self.first_obo_secret, self.first_obo_code)
        self.second_obo_scope = "openid%20/read-limited%20/activities/update%20/person/update"
        self.second_obo_code = self.generate_auth_code(self.second_obo_id, self.second_obo_scope, "api2PostUpdateCode")
        self.second_obo_access, self.second_obo_refresh, self.second_obo_id_token = self.orcid_exchange_auth_token(self.second_obo_id, self.second_obo_secret, self.second_obo_code)

    def get_id_token(self, token, id, secret):
        self.assertIsNotNone(token,"Bearer not recovered: " + str(token))
        curl_params = ['-L', '-H', "Accept: application/json", '--data', 'client_id=' + id + '&client_secret=' + secret + '&subject_token=' + token + '&grant_type=urn:ietf:params:oauth:grant-type:token-exchange&subject_token_type=urn:ietf:params:oauth:token-type:access_token&requested_token_type=urn:ietf:params:oauth:token-type:id_token']
        response = self.orcid_curl("https://" + properties.test_server + "/oauth/token", curl_params)
        return response

    def get_obo_token(self, token, id, secret):
        curl_params = ['-L', '-H', "Accept: application/json", '--data', 'client_id=' + id + '&client_secret=' + secret +
                     '&grant_type=urn:ietf:params:oauth:grant-type:token-exchange&subject_token=' + token +
                     '&subject_token_type=urn:ietf:params:oauth:token-type:id_token&requested_token_type=urn:ietf:params:oauth:token-type:access_token']

        response = self.orcid_curl("https://" + self.test_server + "/oauth/token", curl_params)
        return response

    def test_010_existing_token_flow(self):
        id_token_response = self.get_id_token(self.first_obo_access, self.first_obo_id, self.first_obo_secret)
        id_token = json.loads(id_token_response)
        self.assertTrue(id_token['access_token'], "Unable to generate id_token from existing token: " + id_token_response)
        obo_token_response = self.get_obo_token(id_token['access_token'], self.second_obo_id, self.second_obo_secret)
        obo_token = json.loads(obo_token_response)
        self.assertTrue(obo_token['access_token'], "Unable to generate OBO Token: " + obo_token_response)
        OauthOpenId.obo_token = obo_token['access_token']

    def test_011_openid_post_work(self):
        response = self.post_member_obo(OauthOpenId.obo_token,self.version, "work", "ma30_work_member_obo.xml")
        response_error = "409 Conflict: The item has a limited or private visibility and your request doesn't have the required scope."
        self.assertTrue(response_error in response, "Expected error is missing: " + response)

    def test_012_full_scope_obo(self):
        obo_token_response = self.get_obo_token(self.second_obo_id_token, self.first_obo_id, self.first_obo_secret)
        obo_token = json.loads(obo_token_response)
        self.assertTrue(obo_token['access_token'], "Unable to generate OBO Token: " + obo_token_response)
        OauthOpenId.obo_token = obo_token['access_token']

    def test_013_full_scope_post_work(self):
        response = self.post_member_obo(OauthOpenId.obo_token, self.version, "work", "ma30_work_member_obo.xml")
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.obo_token, '-H', 'Accept: application/xml','-X', 'GET']
        url = "api." + properties.test_server + "/v3.0/%s/work/" % (self.orcid_id)
        search_pattern = "%s(\d+)" % url
        putcode = re.search(search_pattern, re.sub('[\s+]', '', response))
        url = "https://" + url + putcode.group(1)
        read_response = self.orcid_curl(url, curl_params)
        assertion_check = "<common:assertion-origin-name>Member OBO Second Client</common:assertion-origin-name>"
        self.assertTrue(assertion_check in read_response, "Unexpected result: " + read_response)