import OrcidBaseTest
import properties

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.client_id     = properties.memberClientId
        self.client_secret = properties.memberClientSecret
        self.notify_token  = properties.notifyToken
        self.orcid_id      = properties.orcidId
        self.version	   = "/v2.1/"
        self.scope               = "/read-limited%20/activities/update%20/person/update"
        self.code                = self.generate_auth_code(self.client_id,self.scope, "api2PostUpdateCode")
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)

    
    def test_post_update_work(self):
        # Test Post the ma test work 2
        response = self.post_activity(self.version, "work", "ma21_work.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        print putcode
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # Update the work with JSON
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = '{"put-code":' + str(putcode) + ',"title":{"title":"APITestTitleUpdated21"},"type":"JOURNAL_ARTICLE","external-ids":{"external-id":[{"external-id-value":"4321","external-id-type":"doi","external-id-relationship":"SELF"}]}}'
        update_response = self.update_activity(self.version, putcode, updated_data, "work")
        self.assertTrue("200 OK" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
        
        
    def test_post_education(self):
        # Test Post education item to the record created today using the 2.1 api 
        response = self.post_activity(self.version, "education", "ma21_edu.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_funding(self):
		# Test Post funding to the record created today using the 2.1 api 
        response = self.post_activity(self.version, "funding", "ma21_fund2.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_peerreview(self):
		# Test Post peer review to the record created today using the 2.1 api 
        response = self.post_activity(self.version, "peer-review", "ma21_peer2.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_update_keyword(self):
        # Test Post keyword to the record created today using the 2.1 api and test updating using put
        response = self.post_activity(self.version, "keywords", "ma21_keyword.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        #Update the keyword from Kiwi to grapes
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = '{"put-code":' + str(putcode) + ',"content":"grapes"}'
        update_response = self.update_activity(self.version, putcode, updated_data, "keywords")
        self.assertTrue("200 OK" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
             
    def test_post_othername(self):
		# Test post other name to the record created today using the 2.1 api
        response = self.post_activity(self.version, "other-names", "ma21_othername.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_country(self):
		# Test Post country to the record created today using the 2.1 api
        response = self.post_activity(self.version, "address", "ma21_country.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_website(self):
		# Test Post website to the record created today using the 2.1 api
        response = self.post_activity(self.version, "researcher-urls", "ma21_website.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_identifier(self):
        # Test Post personal identifier to the record created today using the 2.1 api
        response = self.post_activity(self.version, "external-identifiers", "ma21_identifier.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)     

    def test_post_update_notification(self):
		# Test Post notification to the record created today using the 2.1 api
        self.access = self.notify_token
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        # Test Post a notification to the record created for testing today. Use the existing notify token.
        response = self.post_activity(self.version, "notification-permission", "ma21_notify.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)

    def test_post_bulk_works(self):
        # Post a bulk works item using 2.1 api to the record created for testing today
        response = self.post_activity(self.version, "works", "ma20_bulkworks.xml")
        self.assertTrue("200 OK" in response, "Response missing \"Created\" tag: " + response)
        
        
