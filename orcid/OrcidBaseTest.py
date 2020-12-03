import unittest
import subprocess
import json
import os.path
import urllib
import properties
import local_properties
from OrcidBrowser import OrcidBrowser

class OrcidBaseTest(unittest.TestCase):

    secrets_file_path = './'
    secrets_file_extension = '.secret'
    xml_data_files_path = 'post_files/'

    if local_properties.type == "jenkins":
        try:
            username = properties.user_login
            password = properties.password
            test_server = properties.test_server
        except AttributeError:
            username = ""
            password = ""
            test_server = ""
    else:
        username = local_properties.username
        password = local_properties.password
        test_server = local_properties.test_server

    def orcid_curl(self, url, curl_opts):
        curl_call = ["curl"] + curl_opts + [url]
        try:
            p = subprocess.Popen(curl_call, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(subprocess.list2cmdline(curl_call))
            output,err = p.communicate()
            return output
        except Exception as e:
            raise Exception(e)

    def save_secrets_to_file(self, content, code):
        with open(os.path.join(self.secrets_file_path, code + self.secrets_file_extension), 'w') as secrets_file:
            json.dump(content, secrets_file)

    def load_secrets_from_file(self, code):
        content = None
        with open(os.path.join(self.secrets_file_path, code + self.secrets_file_extension), 'r') as secrets_file:
            content = json.load(secrets_file)
        return content

    def generate_auth_code_bash(self, public_client_id, scope, auth_code_name="readPublicCode"):
        cmd = [properties.authCodeGenerator, self.username + '%40mailinator.com', self.password, client_id, scope]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output,err = p.communicate()
        print(subprocess.list2cmdline(cmd).strip())
        code = str(output).strip()
        return code

    def generate_auth_code_selenium(self, public_client_id, scope, auth_code_name="readPublicCode"):
        firefox = OrcidBrowser()
        code = firefox.getAuthCode(self.username,self.password,public_client_id,scope)
        firefox.bye()
        return code

    def generate_implicit_code_selenium(self, public_client_id, scope, auth_code_name="readPublicCode"):
        firefox = OrcidBrowser()
        code = firefox.getImplicitToken(self.username,self.password,public_client_id,scope)
        firefox.bye()
        return code

    def generate_implicit_code_selenium(self, public_client_id, scope, auth_code_name="readPublicCode"):
        firefox = OrcidBrowser()
        code = firefox.getImplicitToken(properties.user_login,properties.user_pass,public_client_id,scope)
        firefox.bye()
        return code

    def generate_auth_code(self, client_id, scope, auth_code_name="readPublicCode"):
        # returns [No JSON object could be decoded | 6 digits ]
        who = str(auth_code_name) + "_" + client_id
        if not os.path.isfile(os.path.join(self.secrets_file_path, who + self.secrets_file_extension)):
            code = self.generate_auth_code_selenium(client_id, scope, auth_code_name="readPublicCode")
            if code:
                self.save_secrets_to_file(code, who)
            print "Using fresh code: %s" % code
            return code
        else:
            code = self.load_secrets_from_file(who)
            code = str(code).strip()
            print "Using local code: %s" % code
            return code

    def orcid_exchange_auth_token(self, client_id, client_secret, code):
        if not code:
            return [None, None]
        json_response = None
        if not os.path.isfile(os.path.join(self.secrets_file_path, code + self.secrets_file_extension)):
            exchange_data = ["-L", "-H", "Accept: application/json", "--data", "client_id=" + client_id + "&client_secret=" + client_secret + "&grant_type=authorization_code" + "&code=" + code + "&redirect_uri=https://developers.google.com/oauthplayground"]
            response = self.orcid_curl("https://pub." + self.test_server + "/oauth/token", exchange_data)
            json_response = json.loads(response)
        else:
            json_response = self.load_secrets_from_file(code)
        if(('access_token' in json_response) & ('refresh_token' in json_response)):
            self.save_secrets_to_file(json_response, code)
            if ('id_token' in json_response):
                return [json_response['access_token'], json_response['refresh_token'], json_response['id_token']]
            else:
                return [json_response['access_token'], json_response['refresh_token']]
        else: 
            if('error' in json_response):
                raise ValueError("No tokens found in response: " + json_response['error']['value'])
        return [None, None]

    def orcid_generate_token(self, client_id, client_secret, scope="/read-public"):
        data = ['-L', '-H', 'Accept: application/json', '-d', "client_id=" + client_id, '-d', "client_secret=" + client_secret, '-d', 'scope=' + scope, '-d', 'grant_type=client_credentials']
        response = self.orcid_curl("https://" + self.test_server + "/oauth/token", data)
        json_response = json.loads(response)
        if('access_token' in json_response):
            return json_response['access_token']
        else: 
            if('error' in json_response):
                print "No access token found in response: " + json_response['error']['value']
        return None

    def orcid_generate_member_token(self, client_id, client_secret, scope="/read-public"):
        data = ['-L', '-H', 'Accept: application/json', '-d', "client_id=" + client_id, '-d', "client_secret=" + client_secret, '-d', 'scope=' + scope, '-d', 'grant_type=client_credentials']
        response = self.orcid_curl("https://api." + self.test_server + "/oauth/token", data)
        json_response = json.loads(response)
        if('access_token' in json_response):
            return json_response['access_token']
        else: 
            if('error' in json_response):
                raise ValueError("No access token found in response: " + json_response['error']['value'])
        return [None, None]

    def orcid_refresh_token(self, client_id, client_secret, access_token, refresh_token, scope="/read-limited%20/activities/update", revoke_old="false"):
        data = ['-L', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(access_token), '-d', "client_id=" + client_id, '-d', "client_secret=" + client_secret, '-d', "refresh_token=" + refresh_token, '-d', 'scope=' + scope, '-d', "revoke_old=" + revoke_old, '-d', 'grant_type=refresh_token']
        response = self.orcid_curl("https://api." + self.test_server + "/oauth/token", data)
        json_response = json.loads(response)
        if('access_token' in json_response):
            return json_response['access_token']
        elif('Parent token is disabled' in str(json_response)):
            return json_response
        else: 
            if('error' in json_response):
                raise ValueError("No access token found in response: " + json_response['error']['value'])
		return [None, None]

    def orcid_refresh_token(self, client_id, client_secret, access_token, refresh_token, scope="/read-limited%20/activities/update", revoke_old="false"):
        data = ['-L', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(access_token), '-d', "client_id=" + client_id, '-d', "client_secret=" + client_secret, '-d', "refresh_token=" + refresh_token, '-d', 'scope=' + scope, '-d', "revoke_old=" + revoke_old, '-d', 'grant_type=refresh_token']
        response = self.orcid_curl("https://api." + self.test_server + "/oauth/token", data)
        json_response = json.loads(response)
        if('access_token' in json_response):
            return json_response['access_token']
        elif('Parent token is disabled' in str(json_response)):
            return json_response
        else: 
            if('error-desc' in json_response):
                raise ValueError("No access token found in response: " + json_response['error-desc']['value'])
        return [None, None]

    def remove_by_putcode(self, version, putcode, activity_type = "work"):
        print "Deleting putcode: %s" % putcode
        curl_params = ['-L', '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml','-H', 'Authorization: Bearer ' + str(self.token), '-X', 'DELETE']
        try:
            response = self.orcid_curl("https://api." + self.test_server + version + "%s/%s/%s" % (self.orcid_id, activity_type, putcode), curl_params)
            return response
        except Exception as e:
            print "We've got some problems while deleting by putcode: " + e
        return ""

    def get_putcode_from_response(self, response):
        for header in response.split('\n'):
            if("Location:" in header):
                location_chunks = header.split('/')
                return location_chunks[-1]
        return False

    def post_activity(self, version, activity_type = "work", xml_file = "ma2_work.xml"):
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xml_file, '-X', 'POST']
        response = self.orcid_curl("https://api." + self.test_server + version + "%s/%s" % (self.orcid_id, activity_type) , curl_params)
        return response

    def post_user_obo(self, version, activity_type = "work", xml_file = "ma2_work.xml"):
        self.assertIsNotNone(self.user_obo_access,"Bearer not recovered: " + str(self.user_obo_access))
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(self.user_obo_access), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xml_file, '-X', 'POST']
        response = self.orcid_curl("https://api." + self.test_server + version + "%s/%s" % (self.orcid_id, activity_type) , curl_params)
        return response

    def post_member_obo(self, token, version, activity_type = "work", xml_file = "ma2_work.xml"):
        self.assertIsNotNone(token,"Bearer not recovered: " + str(token))
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(token), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xml_file, '-X', 'POST']
        response = self.orcid_curl("https://api." + self.test_server + version + "%s/%s" % (self.orcid_id, activity_type) , curl_params)
        return response

    def post_user_obo(self, version, activity_type = "work", xml_file = "ma2_work.xml"):
        self.assertIsNotNone(self.user_obo_access,"Bearer not recovered: " + str(self.user_obo_access))
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(self.user_obo_access), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xml_file, '-X', 'POST']
        response = self.orcid_curl("https://api." + properties.test_server + version + "%s/%s" % (self.orcid_id, activity_type) , curl_params)
        return response

    def post_member_obo(self, token, version, activity_type = "work", xml_file = "ma2_work.xml"):
        self.assertIsNotNone(token,"Bearer not recovered: " + str(token))
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(token), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xml_file, '-X', 'POST']
        response = self.orcid_curl("https://api." + properties.test_server + version + "%s/%s" % (self.orcid_id, activity_type) , curl_params)
        return response

    def update_activity(self, version, putcode, updated_data, activity_type = "work"):
        update_curl_params = ['-i', '-L', '-k', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-d', updated_data, '-X', 'PUT']
        update_response = self.orcid_curl("https://api." + self.test_server + version + "%s/%s/%d" % (self.orcid_id, activity_type, int(putcode)), update_curl_params)
        return update_response

    def delete_activity(self, version, putcode, activity_type = "work"):
        delete_curl_params = ['-i', '-L', '-k', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-X', 'DELETE']
        delete_response = self.orcid_curl("https://api." + self.test_server + version + "%s/%s/%d" % (self.orcid_id, activity_type, int(putcode)), delete_curl_params)
        return delete_response

    def read_record(self, version, token, endpoint = "record"):
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(token), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + version + "%s/%s" % (self.orcid_id, endpoint) , curl_params)
        return response

    def post_activity_refresh(self, version, access_token, activity_type = "work", xml_file = "ma2_work.xml"):
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(access_token), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xml_file, '-X', 'POST']
        response = self.orcid_curl("https://api." + self.test_server + version + "%s/%s" % (self.orcid_id, activity_type) , curl_params)
        return response

    def read_record(self, version, token, endpoint = "record"):
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(token), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + version + "%s/%s" % (self.orcid_id, endpoint) , curl_params)
        return response

    def post_activity_refresh(self, version, access_token, activity_type = "work", xml_file = "ma2_work.xml"):
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(access_token), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xml_file, '-X', 'POST']
        response = self.orcid_curl("https://api." + self.test_server + version + "%s/%s" % (self.orcid_id, activity_type) , curl_params)
        return response

