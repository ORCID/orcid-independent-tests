import OrcidBaseTest
import properties
import local_properties

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.version = "/v2.0/"
        if properties.type == "actions":
          self.client_id = properties.memberClientId
          self.client_secret = properties.memberClientSecret
          self.notify_token = properties.notifyToken
          self.orcid_id = properties.orcidId
          self.scope = "/read-limited%20/activities/update%20/person/update"
          self.code = self.generate_auth_code(self.client_id, self.scope)
          self.access, self.refresh = self.orcid_exchange_auth_token(self.client_id, self.client_secret, self.code)
          print ("Using code: %s | access: %s " % (self.code, self.access))
        else:
          self.client_id = local_properties.step_2_client_id
          self.client_secret = local_properties.step_2_client_secret
          self.notify_token = local_properties.notify_token
          self.orcid_id = local_properties.orcid_id_member
          self.scope = "/read-limited%20/activities/update%20/person/update"
          self.code = self.generate_auth_code(self.client_id, self.scope)
          self.access, self.refresh = self.orcid_exchange_auth_token(self.client_id, self.client_secret, self.code)

    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_0/crud_work_v20.cy.js  
        
    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_0/crud_education_v20.cy.js
        
    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_0/crud_funding_v20.cy.js
        
    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_0/crud_peerReview_v20.cy.js
        
    def test_post_update_keyword(self):
        # Test Post keyword to the record created today using the 2.0 api and test updating using put
        response = self.post_activity(self.version, "keywords", "ma2_keyword.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"201\" code: " + response)
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
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"201\" code: " + response) 
        
    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_0/crud_address_v20.cy.js    
        
    def test_post_website(self):
		# Test Post website to the record created today using the 2.0 api
        response = self.post_activity(self.version, "researcher-urls", "ma2_website.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"201\" code: " + response) 
        
    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_0/crud_externalids_v20.cy.js     

    def test_post_update_notification(self):
		# Test Post notification to the record created today using the 2.0 api
        self.access = self.notify_token
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        # Test Post a notification to the record created for testing today. Use the existing notify token.
        response = self.post_activity(self.version, "notification-permission", "ma2_notify.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"201\" code: " + response)
        
        
