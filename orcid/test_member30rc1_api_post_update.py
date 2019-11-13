import OrcidBaseTest
import properties
import test_type

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
      self.version = "/v3.0_rc1/"
      if (test_type.arg == "jenkins"):
        self.client_id = properties.memberClientId
        self.client_secret = properties.memberClientSecret
        self.notify_token = properties.notifyToken
        self.webhook_access = self.orcid_generate_token(self.client_id, self.client_secret, "/webhook")
        # Comment out below when testing locally
        self.orcid_id = properties.orcidId
        self.scope = "/read-limited%20/activities/update%20/person/update"
        self.code = self.generate_auth_code(self.client_id, self.scope, "api2PostUpdateCode")
        self.access, self.refresh = self.orcid_exchange_auth_token(self.client_id, self.client_secret, self.code)
        # Use below when testing locally
      else:
        self.access = "299e0132-623d-4024-9b47-6c9a0e042b39"
        self.orcid_id = "0000-0001-6009-1985"
        self.webhook_access = "af36161d-0971-4ac6-b860-5bb3f7cdef64"
        self.notify_token = "eafafe49-b5bf-41db-9fb5-ad3a6cba575b"


    
    def test_post_update_work(self):
        #Post a work using 3.0_rc1 to the record created for testing today
        response = self.post_activity(self.version, "work", "ma30rc1_work.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        print putcode
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        #Update the work with JSON
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = '{"put-code":' + str(putcode) + ',"title":{"title":"APITestTitleUpdated21"},"type":"journal-article","external-ids":{"external-id":[{"external-id-value":"1111","external-id-type":"doi","external-id-relationship":"self"}]}}'
        update_response = self.update_activity(self.version, putcode, updated_data, "work")
        self.assertTrue("200 OK" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
        
        
    def test_post_education(self):
        # Post an education item using 3.0_rc1 to the record created for testing today
     #   response = self.post_activity(self.version, "education", "ma30rc1_edu.xml")
        response = "a"
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + self.access + " " + self.client_id)
        
    def test_post_qualification(self):
        # Post a qualification item using 3.0_rc1 to the record created for testing today
        response = self.post_activity(self.version, "qualification", "ma30rc1_qualify.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_funding(self):
    	# Post a funding itme using 3.0_rc1 to the record created for testing today
        response = self.post_activity(self.version, "funding", "ma30rc1_fund2.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_peerreview(self):
    	# Post a peer-review using 3.0_rc1 to the record created for testing today
        response = self.post_activity(self.version, "peer-review", "ma30rc1_peer2.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_researchresource(self):
    	# Post a research-resource itme using 3.0_rc1 to the record created for testing today
        response = self.post_activity(self.version, "research-resource", "ma30rc1_rr.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_update_keyword(self):
        # Post a keyword using 3.0_rc1 to the record created for testing today
        response = self.post_activity(self.version, "keywords", "ma30rc1_keyword.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        #Update the keyword from pear to grapes
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = '{"put-code":' + str(putcode) + ',"content":"peaches"}'
        update_response = self.update_activity(self.version, putcode, updated_data, "keywords")
        self.assertTrue("200 OK" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
             
    def test_post_othername(self):
    	# Post an other name using 3.0_rc1 to the record created for testing today
        response = self.post_activity(self.version, "other-names", "ma30rc1_othername.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_country(self):
    	# Post a country using 3.0_rc1 to the record created for testing today
        response = self.post_activity(self.version, "address", "ma30rc1_country.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_website(self):
    	# Post a website using 3.0_rc1 to the record created for testing today
        response = self.post_activity(self.version, "researcher-urls", "ma30rc1_website.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_identifier(self):
        # Post a person identifier using 3.0_rc1 to the record created for testing today
        response = self.post_activity(self.version, "external-identifiers", "ma30rc1_identifier.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)   

    def test_post_update_notification(self):
        self.access = self.notify_token
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        # Post a notification using 3.0_rc1 to the record created for testing today. Use the existing notify token.
        response = self.post_activity(self.version, "notification-permission", "ma30rc1_notify.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)

    def test_post_bulk_works(self):
        # Post a bulk works item using 3.0_rc1 to the record created for testing today
        response = self.post_activity(self.version, "works", "ma30rc1_bulkworks.xml")
        self.assertTrue("200 OK" in response, "Response missing \"Created\" tag: " + response)
	self.assertFalse("400 Bad Request" in response, "badly formed XML error in response " + response)
	self.assertFalse("409 Conflict" in response, "Already posted this work error in response " + response)
        
        
