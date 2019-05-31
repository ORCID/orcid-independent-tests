import OrcidBaseTest
import properties

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.client_id     = properties.memberClientId
        self.client_secret = properties.memberClientSecret
        self.notify_token  = properties.notifyToken
        self.webhook_access= self.orcid_generate_token(self.client_id, self.client_secret, "/webhook")
        self.version	   = "/v3.0/"
        #Comment out below when testing locally
        self.orcid_id      = properties.orcidId
        self.scope               = "/read-limited%20/activities/update%20/person/update"
        self.code                = self.generate_auth_code(self.client_id,self.scope, "api2PostUpdateCode")
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
        #Use below when testing locally
		#self.access = ""
		#self.orcid_id = ""
    
    def test_post_update_work(self):
        #Post a work using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "work", "ma30_work.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        print putcode
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        #Update the work with JSON
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = '{"put-code":' + str(putcode) + ',"title":{"title":"APITestTitleUpdated30"},"type":"journal-article","external-ids":{"external-id":[{"external-id-value":"16","external-id-type":"doi","external-id-relationship":"self"}]}}'
        update_response = self.update_activity(self.version, putcode, updated_data, "work")
        self.assertTrue("200 OK" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
        
        
    def test_post_education(self):
        # Post an education item using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "education", "ma30_edu.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_qualification(self):
        # Post a qualification item using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "qualification", "ma30_qualify.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_funding(self):
    	# Post a funding itme using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "funding", "ma30_fund.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_peerreview(self):
    	# Post a peer-review using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "peer-review", "ma30_peer.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_researchresource(self):
    	# Post a research-resource itme using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "research-resource", "ma30_rr.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_update_keyword(self):
        # Post a keyword using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "keywords", "ma30_keyword.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        #Update the keyword from pear to grapes
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = '{"put-code":' + str(putcode) + ',"content":"apricots"}'
        update_response = self.update_activity(self.version, putcode, updated_data, "keywords")
        self.assertTrue("200 OK" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
             
    def test_post_othername(self):
    	# Post an other name using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "other-names", "ma30_othername.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_country(self):
    	# Post a country using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "address", "ma30_country.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_website(self):
    	# Post a website using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "researcher-urls", "ma30_website.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response) 
        
    def test_post_identifier(self):
        # Post a person identifier using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "external-identifiers", "ma30_identifier.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)   

    def test_post_update_notification(self):
        self.access = self.notify_token
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        # Post a notification using 3.0 to the record created for testing today. Use the existing notify token.
        response = self.post_activity(self.version, "notification-permission", "ma30_notify.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        
    def test_post_webhook(self):
    #Post a webhook for the ORCID iD. This test is not version dependent
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.webhook_access, '-H', 'Content-Length: 0', '-H', 'Accept: application/json', '-k', '-X', 'PUT']
        response = self.orcid_curl("http://api." + properties.test_server + "/%s/webhook/%s" % (self.orcid_id, "http%3A%2F%2Fnowhere3.com%2Fupdated"), curl_params)
        self.assertTrue("201 Created" in response, "response: " + response)
        
    def test_post_bulk_works(self):
        # Post a bulk works item using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "works", "ma30_bulkworks.xml")
        self.assertTrue("200 OK" in response, "Response missing \"Created\" tag: " + response)
	self.assertFalse("400 Bad Request" in response, "badly formed XML error in response " + response)
	self.assertFalse("409 Conflict" in response, "Already posted this work error in response " + response)
        
