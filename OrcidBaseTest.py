import unittest
import subprocess
import json

class OrcidBaseTest(unittest.TestCase):

    def orcid_curl(self, url, curl_opts):
        curl_call = ["curl"] + curl_opts + [url]
        p = subprocess.Popen(curl_call, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output,err = p.communicate()
        return output

    def orcid_generate_read_public_token(self, client_id, client_secret):
        data = ['-L', '-H', 'Accept: application/json', '-d', "client_id=" + client_id, '-d', "client_secret=" + client_secret, '-d', 'scope=/read-public', '-d', 'grant_type=client_credentials']
        response = self.orcid_curl("http://pub.qa.orcid.org/oauth/token", data)
        json_response = json.loads(response)
        return json_response['access_token']
        
        
        