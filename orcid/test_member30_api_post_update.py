import OrcidBaseTest
import properties
import local_properties

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
      self.version = "/v3.0/"
      if local_properties.type == "jenkins":
        self.client_id     = properties.memberClientId
        self.client_secret = properties.memberClientSecret
        self.notify_token  = properties.notifyToken
        self.webhook_access= self.orcid_generate_token(self.client_id, self.client_secret, "/webhook")
        self.orcid_id      = properties.orcidId
        self.scope               = "/read-limited%20/activities/update%20/person/update"
        self.code                = self.generate_auth_code(self.client_id,self.scope, "api2PostUpdateCode")
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)

        self.user_obo_id = "APP-52PDPI669AHFVT3V"
        self.user_obo_secret = "8e242970-5d2a-4b47-b7d3-c88165a10bfb"
        self.user_obo_scope = "openid%20/read-limited%20/activities/update%20/person/update"
        self.user_obo_code = self.generate_auth_code(self.user_obo_id, self.user_obo_scope, "api2PostUpdateCode")
        self.user_obo_access, self.user_obo_refresh = self.orcid_exchange_auth_token(self.user_obo_id, self.user_obo_secret, self.user_obo_code)
      else:
        self.orcid_id = local_properties.orcid_id_member
        self.access = local_properties.access_member
        self.notify_token = local_properties.notify_token
        self.webhook_access = local_properties.webhook
        self.user_obo_id = "APP-52PDPI669AHFVT3V"
        self.user_obo_secret = "8e242970-5d2a-4b47-b7d3-c88165a10bfb"
        self.user_obo_scope = "openid%20/read-limited%20/activities/update%20/person/update"
        self.user_obo_code = self.generate_auth_code(self.user_obo_id, self.user_obo_scope, "api2PostUpdateCode")
        self.user_obo_access, self.user_obo_refresh = self.orcid_exchange_auth_token(self.user_obo_id, self.user_obo_secret, self.user_obo_code)

    
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

   # def test_user_obo(self):
    def test_USER_OBO(self):
        #Post a work using 3.0 to the record created for testing today
        response = self.post_user_obo(self.version, "work", "ma21_work.xml")
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)

    def post_user_obo(self, version, activity_type = "work", xml_file = "ma2_work.xml"):
        self.assertIsNotNone(self.user_obo_access,"Bearer not recovered: " + str(self.user_obo_access))
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(self.user_obo_access), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xml_file, '-X', 'POST']
        response = self.orcid_curl("https://api." + properties.test_server + version + "%s/%s" % (self.orcid_id, activity_type) , curl_params)
        return response
