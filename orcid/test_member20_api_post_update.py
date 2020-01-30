import OrcidBaseTest
import properties

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.client_id              = properties.memberClientId
        self.client_secret          = properties.memberClientSecret
        self.notify_token           = properties.notifyToken
        self.orcid_id               = properties.orcidId
        self.version	            = "/v2.0/"
        self.scope                  = "/read-limited%20/activities/update%20/person/update"
        self.code                   = self.generate_auth_code(self.client_id,self.scope, "api2PostUpdateCode")
        self.access,self.refresh    = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
        print "Using code: %s | access: %s " % (self.code,self.access)

    def test_post_update_work(self):
        # Test Post the ma test work 2
        response = self.post_activity(self.version, "work", "ma2_work.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        print putcode
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # Update the work with JSON
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = '{"put-code":' + str(putcode) + ',"title":{"title":"APITestTitleUpdated"},"type":"JOURNAL_ARTICLE","external-ids":{"external-id":[{"external-id-value":"1234","external-id-type":"doi","external-id-relationship":"SELF"}]}}'
        update_response = self.update_activity(self.version, putcode, updated_data, "work")
        self.assertTrue("HTTP/1.1 200" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
        
        
    def test_post_education(self):
        # Test Post education item to the record created today using the 2.0 api 
        response = self.post_activity(self.version, "education", "ma2_edu.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_funding(self):
		# Test Post funding to the record created today using the 2.0 api 
        response = self.post_activity(self.version, "funding", "ma2_fund2.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_peerreview(self):
		# Test Post peer review to the record created today using the 2.0 api 
        response = self.post_activity(self.version, "peer-review", "ma2_peer2.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_update_keyword(self):
        # Test Post keyword to the record created today using the 2.0 api and test updating using put
        response = self.post_activity(self.version, "keywords", "ma2_keyword.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        #Update the keyword from keyword to oranges
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = '{"put-code":' + str(putcode) + ',"content":"oranges"}'
        update_response = self.update_activity(self.version, putcode, updated_data, "keywords")
        self.assertTrue("HTTP/1.1 200" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
             
    def test_post_othername(self):
		# Test Post other name to the record created today using the 2.0 api
        response = self.post_activity(self.version, "other-names", "ma2_othername.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_country(self):
		# Test Post country to the record created today using the 2.0 api
        response = self.post_activity(self.version, "address", "ma2_country.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_website(self):
		# Test Post website to the record created today using the 2.0 api
        response = self.post_activity(self.version, "researcher-urls", "ma2_website.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_identifier(self):
        # Test Post personal identifier to the record created today using the 2.0 api
        response = self.post_activity(self.version, "external-identifiers", "ma2_identifier.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"Created\" tag: " + response)     

    def test_post_update_notification(self):
		# Test Post notification to the record created today using the 2.0 api
        self.access = self.notify_token
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        # Test Post a notification to the record created for testing today. Use the existing notify token.
        response = self.post_activity(self.version, "notification-permission", "ma2_notify.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"Created\" tag: " + response)
        
        
