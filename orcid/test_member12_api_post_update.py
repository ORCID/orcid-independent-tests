import OrcidBaseTest
import pyjavaproperties

class Member12ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):
    
    xml_data_files_path = '../ORCID-Source/orcid-integration-test/src/test/manual-test/'

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test.properties'))
        self.orcid_props   = p
        self.client_id     = self.orcid_props['memberClientId']
        self.client_secret = self.orcid_props['memberClientSecret']        
        self.code          = self.orcid_props['api1PostUpdateCode']
        self.orcid_id      = self.orcid_props['orcidId']
        self.webhook_access= self.orcid_props['webhookToken']
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)

    def test_post_work(self):
        self.assertIsNotNone(self.access, "Not token generated: [%s]" % str(self.access))
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma_work.xml', '-X', 'POST']
        response = self.orcid_curl("http://api.qa.orcid.org/v1.2/%s/orcid-works" % self.orcid_id, curl_params)
        self.assertTrue("201 Created" in response, "response: " + response)

    def test_update_work(self):
        self.assertIsNotNone(self.access, "Not token generated: [%s]" % str(self.access))
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma_work2.xml', '-X', 'PUT']
        response = self.orcid_curl("http://api.qa.orcid.org/v1.2/%s/orcid-works" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)

    def test_post_funding(self):
        self.assertIsNotNone(self.access, "Not token generated: [%s]" % str(self.access))
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma_fund.xml', '-X', 'POST']
        response = self.orcid_curl("http://api.qa.orcid.org/v1.2/%s/funding" % self.orcid_id, curl_params)
        self.assertTrue("201 Created" in response, "response: " + response)

    def test_update_funding(self):
        self.assertIsNotNone(self.access, "Not token generated: [%s]" % str(self.access))
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma_fund2.xml', '-X', 'PUT']
        response = self.orcid_curl("http://api.qa.orcid.org/v1.2/%s/funding" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)

    def test_post_education(self):
        self.assertIsNotNone(self.access, "Not token generated: [%s]" % str(self.access))
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma_edu.xml', '-X', 'POST']
        response = self.orcid_curl("http://api.qa.orcid.org/v1.2/%s/affiliations" % self.orcid_id, curl_params)
        self.assertTrue("201 Created" in response, "response: " + response)

    def test_update_education(self):
        self.assertIsNotNone(self.access, "Not token generated: [%s]" % str(self.access))
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma_edu2.xml', '-X', 'PUT']
        response = self.orcid_curl("http://api.qa.orcid.org/v1.2/%s/affiliations" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)

    def test_post_bio(self):
        self.assertIsNotNone(self.access, "Not token generated: [%s]" % str(self.access))
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma_bio.xml', '-X', 'PUT']
        response = self.orcid_curl("http://api.qa.orcid.org/v1.2/%s/orcid-bio" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)

    '''def test_revoke_post_work(self):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma_work.xml', '-X', 'POST']
        response = self.orcid_curl("http://api.qa.orcid.org/v1.2/%s/orcid-works" % self.orcid_id, curl_params)
        self.assertTrue("401 Unauthorized" in response, "response: " + response)'''

    '''def test_post_webhook(self):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.webhook_access, '-H', 'Content-Length: 0', '-H', 'Accept: application/json', '-k', '-X', 'PUT']
        response = self.orcid_curl("http://api.qa.orcid.org/%s/webhook/%s" % (self.orcid_id, "http%3A%2F%2Fnowhere3.com%2Fupdated"), curl_params)
        self.assertTrue("201 Created" in response, "response: " + response)'''
