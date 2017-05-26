import OrcidBaseTest
import pyjavaproperties
import properties.py

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        #self.client_id     = self.orcid_props['memberClientId']
        #self.client_secret = self.orcid_props['memberClientSecret']
        #self.notify_token  = self.orcid_props['notifyToken']
        #self.code          = self.orcid_props['api2PostUpdateCode']
        #self.orcid_id      = self.orcid_props['orcidId']
        self.code                = self.generate_auth_code(self.client_id, "/orcid-bio/update /orcid-works/create /orcid-works/update /affiliations/create /affiliations/update /funding/create /funding/update /orcid-profile/read-limited")
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
    
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
        
    def test_post_update_delete_keyword(self):
        # TEST 96 post education
        response = self.post_activity("keywords", "ma2_keyword.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # TEST delete
        delete_response = self.delete_activity(putcode, "keywords")
        self.assertTrue("204 No Content" in delete_response, "Delete Action Response: " + delete_response + " using putcode [%s]" % str(putcode))
        
    def test_post_update_delete_identifier(self):
        # TEST 97 post education
        response = self.post_activity("external-identifiers", "ma2_identifier.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # TEST delete
        delete_response = self.delete_activity(putcode, "external-identifiers")
        self.assertTrue("204 No Content" in delete_response, "Delete Action Response: " + delete_response + " using putcode [%s]" % str(putcode))

    def test_post_update_delete_notification(self):
        self.access = self.notify_token
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        # TEST 99 post education
        response = self.post_activity("notification-permission", "notify.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # TEST delete
        delete_response = self.delete_activity(putcode, "notification-permission")
        self.assertTrue("200 OK" in delete_response, "Delete Action Response: " + delete_response + " using putcode [%s]" % str(putcode))        
        
        