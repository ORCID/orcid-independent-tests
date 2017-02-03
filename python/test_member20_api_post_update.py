import OrcidBaseTest
import pyjavaproperties

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):
    
    xml_data_files_path = '../ORCID-Source/orcid-integration-test/src/test/manual-test/'

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test-client.properties'))
        self.orcid_props   = p
        self.client_id     = self.orcid_props['memberClientId']
        self.client_secret = self.orcid_props['memberClientSecret']        
        self.code          = self.orcid_props['api2PostUpdateCode']
        self.orcid_id      = self.orcid_props['orcidId']
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
    '''
    def test_blank(self):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml']
        response = self.orcid_curl("", curl_params)
        self.assertTrue("201 Created" in response, "response: " + response)
    '''

    def test_post_work(self):
        # TEST 85 Post the ma test work 2
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma2_work.xml', '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v2.0_rc3/%s/work" % self.orcid_id, curl_params)
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # TEST 88 Update the work with JSON
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = "'{\"put-code\":\"%d\",\"title\":{\"title\":\"APITestTitleUpdated\"},\"type\":\"JOURNAL_ARTICLE\",\"external-ids\":{\"external-id\":[{\"external-id-value\":\"1234\",\"external-id-type\":\"doi\",\"external-id-relationship\":\"SELF\"}]}}'" % int(putcode)
        update_curl_params = ['-i', '-L', '-k', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-d', updated_data, '-X', 'PUT']
        update_response = self.orcid_curl("https://api.qa.orcid.org/v2.0_rc3/%s/work/%d" % (self.orcid_id,int(putcode)), update_curl_params)
        self.assertTrue("PRINT" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
        # TEST 90 Delete the work

