import OrcidBaseTest
import properties

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.client_id     = properties.memberClientId
        self.client_secret = properties.memberClientSecret
        self.notify_token  = properties.notifyToken
        self.orcid_id      = properties.orcidId
        self.scope               = "/read-limited%20/activities/update%20/person/update"
        self.code                = self.generate_auth_code(self.client_id,self.scope, "api2PostUpdateCode")
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
    
    def test_post_update_work(self):
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
        
        
    def test_post_education(self):
        # TEST 92 post education
        response = self.post_activity("education", "ma2_edu.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_funding(self):
        response = self.post_activity("funding", "ma2_fund2.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_peerreview(self):
        response = self.post_activity("peer-review", "ma2_peer2.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_update_keyword(self):
        # TEST 96
        response = self.post_activity("keywords", "ma2_keyword.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        #Update the keyword
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = '{"put-code":' + str(putcode) + ',"content":"oranges"}'
        update_response = self.update_activity(putcode, updated_data, "keywords")
        self.assertTrue("200 OK" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
             
	def test_post_othername(self):
        response = self.post_activity("external-identifiers", "ma2_othername.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response) 
        
	def test_post_country(self):
        response = self.post_activity("external-identifiers", "ma2_country.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_country(self):
        response = self.post_activity("external-identifiers", "ma2_country.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_identifier(self):
        # TEST 97
        response = self.post_activity("external-identifiers", "ma2_identifier.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)     

    def test_post_update_notification(self):
        self.access = self.notify_token
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        # TEST 99
        response = self.post_activity("notification-permission", "notify.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
        