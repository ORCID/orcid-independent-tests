from os import error
import OrcidBaseTest
import properties
import local_properties

class RevokedToken(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        if properties.type == "actions":
          self.test_server = properties.test_server
        else:
          self.test_server = local_properties.test_server
        self.xml_data_files_path = 'post_files/'
        self.orcid = '0000-0001-6030-9366'
        self.active_token = '0cd1a72e-f655-494a-a844-bf715a572304'
        self.revoked_token = 'a9346877-76d3-47ba-9d42-c1c67c4751e6'
            
    def post(self, file_name, token, endpoint, version):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + token, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + file_name, '-X', 'POST']
        post_response = self.orcid_curl("https://api." + self.test_server + "/%s/%s/%s" % (version, self.orcid, endpoint), curl_params)
        return post_response

    def put(self, updated_file, token, endpoint, putcode, version):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + token, '-H', 'Content-Type: application/vnd.orcid+json', '-H', 'Accept: application/json', '-d', '@' + self.xml_data_files_path + updated_file, '-X', 'PUT']
        put_response = self.orcid_curl("https://api." + self.test_server + "/%s/%s/%s/%s" % (version, self.orcid, endpoint, putcode), curl_params)
        return put_response

    def read(self, token, endpoint, putcode, version):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + token, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
        read_response = self.orcid_curl("https://api." + self.test_server + "/%s/%s/%s/%s" % (version, self.orcid, endpoint, putcode), curl_params)
        return read_response

    def delete(self, token, endpoint, putcode, version):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + token, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'DELETE']
        delete_response = self.orcid_curl("https://api." + self.test_server + "/%s/%s/%s/%s" % (version, self.orcid, endpoint, putcode), curl_params)
        return delete_response
        
    def getputcode(self, post_response):
        for header in post_response.split('\n'):
            if("Location:" in header):
                location_chunks = header.split('/')
                putcode = location_chunks[-1].strip()
                return putcode
        return "No putcode found"
        
    def revoked_token_tests(self, version, file):
        post_response = self.post(file, self.active_token, 'work', version)
        self.assertTrue("HTTP/1.1 201" in post_response, "response: " + post_response)
        putcode = self.getputcode(post_response)

        read_response_revoked = self.read(self.revoked_token, 'work', putcode, version)
        self.assertTrue("Invalid access token" in read_response_revoked, "Expected Invalid access token error, instead: " + read_response_revoked)
        
        post_response_revoked = self.post(file, 'work', self.revoked_token,version)
        self.assertTrue("Invalid access token" in post_response_revoked, "Expected Invalid access token error, instead: " + post_response_revoked)

        put_response_revoked = self.put(file, self.revoked_token, 'work', putcode, version)
        self.assertTrue("Invalid access token" in put_response_revoked, "Expected Invalid access token error, instead: " + put_response_revoked)

        delete_response_revoked = self.delete(self.revoked_token, 'work', putcode, version)
        self.assertTrue("HTTP/1.1 204" in delete_response_revoked, "response: " + delete_response_revoked)
        
    def test_20(self):
        self.revoked_token_tests('v3.0', 'ma30_work.xml')
        self.revoked_token_tests('v2.0', '20postwork.xml') 