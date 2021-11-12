import OrcidBaseTest
from OrcidBrowser import OrcidBrowser
import properties
import json
import re
import local_properties

class ContentNegotiation(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        # 0000-0002-7361-1027
        if properties.type == "actions":
          self.test_server = properties.test_server
          self.orcid_id = properties.staticId
          self.access = properties.staticAccess
        else:
          self.test_server = local_properties.test_server
          self.orcid_id = local_properties.orcid_id
          self.access = local_properties.step_1_access

    def read_record(self, header):
        curl_params = ['-L', '-i', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Accept: ' + header, '-X', 'GET']
        read_response = self.orcid_curl("https://" + self.test_server + "/%s" % (self.orcid_id), curl_params)
        return read_response

    def test_010_xml_call(self):
        response = self.read_record("application/xml")
        self.assertTrue("HTTP/1.1 200" in response, "Invalid response code:\n" + response)
        self.assertTrue("Location: https://pub.%s/v3.0/0000-0002-7361-1027" % (self.test_server) in response, "Location missing:\n" + response)
        self.assertTrue("Content-Type: application/xml" in response, "Incorrect Content-Type:\n" + response)
        self.assertTrue("<common:uri>https://%s/0000-0002-7361-1027</common:uri>" % (self.test_server) in response, 'Unable to find "<common:uri>https://%s/0000-0002-7361-1027</common:uri>"" in the response:\n' % (self.test_server) + response)

    def test_011_json_call(self):
        response = self.read_record("application/orcid+json")
        self.assertTrue("HTTP/1.1 200" in response, "Invalid response code:\n" + response)
        self.assertTrue("Location: https://pub.%s/v3.0/0000-0002-7361-1027" % (self.test_server) in response, "Location missing:\n" + response)
        self.assertTrue("Content-Type: application/orcid+json" in response, "Incorrect Content-Type:\n" + response)
        self.assertTrue('"uri" : "https://%s/0000-0002-7361-1027"' % (self.test_server) in response, 'Unable to find "uri" : "https://%s/0000-0002-7361-1027", in the response:\n' % (self.test_server) + response)

    def test_011_turtle_call(self):
        response = self.read_record("text/turtle")
        self.assertTrue("HTTP/1.1 200" in response, "Invalid response code:\n" + response)
        self.assertTrue("Location: https://pub.%s/experimental_rdf_v1/0000-0002-7361-1027" % (self.test_server) in response, "Location missing:\n" + response)
        self.assertTrue("Content-Type: text/turtle" in response, "Incorrect Content-Type:\n" + response)
        self.assertTrue('<https://%s/0000-0002-7361-1027#orcid-id>' % (self.test_server) in response, 'Unable to find "<https://%s/0000-0002-7361-1027#orcid-id>", in the response:\n' % (self.test_server) + response)