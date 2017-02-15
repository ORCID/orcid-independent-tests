import OrcidBaseTest
import pyjavaproperties

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):
    
    xml_data_files_path = '../ORCID-Source/orcid-integration-test/src/test/manual-test/'

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test.properties'))
        self.orcid_props   = p
        self.client_id     = self.orcid_props['memberClientId']
        self.client_secret = self.orcid_props['memberClientSecret']        
        self.code          = self.orcid_props['api2PostUpdateCode']
        self.orcid_id      = self.orcid_props['orcidId']
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
        
    def post_activity(self, activity_type = "work", xml_file = "ma2_work.xml"):
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xml_file, '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s" % (self.orcid_id, activity_type) , curl_params)
        return response
    
    def update_activity(self, putcode, updated_data, activity_type = "work"):
        update_curl_params = ['-i', '-L', '-k', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-d', updated_data, '-X', 'PUT']
        update_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s/%d" % (self.orcid_id, activity_type,int(putcode)), update_curl_params)
        return update_response
    
    def delete_activity(self, putcode, activity_type = "work"):
        delete_curl_params = ['-i', '-L', '-k', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-X', 'DELETE']
        delete_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s/%d" % (self.orcid_id, activity_type, int(putcode)), delete_curl_params)
        return delete_response
    
    def test_post_update_delete_work(self):
        # TEST 85 Post the ma test work 2
        response = self.post_activity("work", "ma2_work.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # TEST 88 Update the work with JSON
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = '{"put-code":' + str(putcode) + ',"title":{"title":"APITestTitleUpdated"},"type":"JOURNAL_ARTICLE","external-ids":{"external-id":[{"external-id-value":"1234","external-id-type":"doi","external-id-relationship":"SELF"}]}}'
        update_response = self.update_activity(putcode, updated_data, "work")
        self.assertTrue("200 OK" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
        # TEST 90 Delete the work
        delete_response = self.delete_activity(putcode, "work")
        self.assertTrue("204 No Content" in delete_response, "Delete Action Response: " + delete_response + " using putcode [%s]" % str(putcode))
        
    def test_post_update_delete_education(self):
        # TEST 92 post education
        response = self.post_activity("education", "ma2_edu.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # TEST delete
        delete_response = self.delete_activity(putcode, "education")
        self.assertTrue("204 No Content" in delete_response, "Delete Action Response: " + delete_response + " using putcode [%s]" % str(putcode))
        
    def test_post_update_delete_funding(self):
        # TEST 92 post education
        response = self.post_activity("funding", "ma2_fund2.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # TEST delete
        delete_response = self.delete_activity(putcode, "funding")
        self.assertTrue("204 No Content" in delete_response, "Delete Action Response: " + delete_response + " using putcode [%s]" % str(putcode))
        
    def test_post_update_delete_peerreview(self):
        # TEST 92 post education
        response = self.post_activity("peer-review", "ma2_peer2.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # TEST delete
        delete_response = self.delete_activity(putcode, "peer-review")
        self.assertTrue("204 No Content" in delete_response, "Delete Action Response: " + delete_response + " using putcode [%s]" % str(putcode))