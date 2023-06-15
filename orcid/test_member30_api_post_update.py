import OrcidBaseTest
import properties
import re
import local_properties

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):
    def setUp(self):
        self.version = "/v3.0/"
        if properties.type == "actions":
            self.test_server = properties.test_server
            self.client_id     = properties.memberClientId
            self.client_secret = properties.memberClientSecret
            self.notify_token  = properties.notifyToken
            self.webhook_access= self.orcid_generate_token(self.client_id, self.client_secret, "/webhook")
            self.orcid_id      = properties.orcidId
            self.scope               = "/read-limited%20/activities/update%20/person/update"
            self.code                = self.generate_auth_code(self.client_id,self.scope)
            self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)

            self.user_obo_id = properties.OBOUserClientId
            self.user_obo_secret = properties.OBOUserClientSecret
            self.user_obo_scope = "openid%20/read-limited%20/activities/update%20/person/update"
            self.user_obo_code = self.generate_auth_code(self.user_obo_id, self.user_obo_scope)
            self.user_obo_access, self.user_obo_refresh, self.user_obo_id_token = self.orcid_exchange_auth_token(self.user_obo_id, self.user_obo_secret, self.user_obo_code)
        else:
            self.test_server = local_properties.test_server
            self.client_id = local_properties.step_2_client_id
            self.client_secret = local_properties.step_2_client_secret
            self.notify_token = local_properties.notify_token
            self.webhook_access = local_properties.webhook
            self.orcid_id = local_properties.orcid_id_member
            self.scope = "/read-limited%20/activities/update%20/person/update"
            self.code = self.generate_auth_code(self.client_id, self.scope)
            self.access, self.refresh = self.orcid_exchange_auth_token(self.client_id, self.client_secret, self.code)

            self.user_obo_id = local_properties.step_2_user_obo_id
            self.user_obo_secret = local_properties.step_2_user_obo_secret
            self.user_obo_scope = "openid%20/read-limited%20/activities/update%20/person/update"
            self.user_obo_code = self.generate_auth_code(self.user_obo_id, self.user_obo_scope)
            self.user_obo_access, self.user_obo_refresh, self.user_obo_id_token = self.orcid_exchange_auth_token(self.user_obo_id, self.user_obo_secret, self.user_obo_code)
          
    # https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v3_0/crud_work_v30.cy.js
    
    # https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v3_0/crud_education_v30.cy.js
        
    def test_post_qualification(self):
        # Post a qualification item using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "qualification", "ma30_qualify.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"201\" code: " + response)
        
    # https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v3_0/crud_funding_v30.cy.js
        
    # https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v3_0/crud_peerReview_v30.cy.js
        
    # https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v3_0/crud_research_resource_v30.cy.js
        
    # https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v3_0/crud_keywords_v30.cy.js
             
    def test_post_othername(self):
        # Post an other name using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "other-names", "ma30_othername.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"201\" code: " + response) 
        
    # https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v3_0/crud_address_v30.cy.js
        
    def test_post_website(self):
        # Post a website using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "researcher-urls", "ma30_website.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"201\" code: " + response) 
        
    # https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v3_0/crud_externalids_v30.cy.js  

    def test_post_update_notification(self):
        self.access = self.notify_token
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        # Post a notification using 3.0 to the record created for testing today. Use the existing notify token.
        response = self.post_activity(self.version, "notification-permission", "ma30_notify.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"201\" code: " + response)
        
    def test_post_webhook(self):
    #Post a webhook for the ORCID iD. This test is not version dependent
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.webhook_access, '-H', 'Content-Length: 0', '-H', 'Accept: application/json', '-k', '-X', 'PUT']
        response = self.orcid_curl("https://api." + self.test_server + "/%s/webhook/%s" % (self.orcid_id, "https%3A%2F%2Fnowhere3.com%2Fupdated"), curl_params)
        self.assertTrue("HTTP/1.1 201" in response, "response: " + response)
        
    def test_post_bulk_works(self):
        # Post a bulk works item using 3.0 to the record created for testing today
        response = self.post_activity(self.version, "works", "ma30_bulkworks.xml")
        self.assertTrue("HTTP/1.1 200" in response, "Response missing \"200\" code: " + response)
        self.assertFalse("HTTP/1.1 400" in response, "badly formed XML error in response " + response)
        self.assertFalse("HTTP/1.1 409" in response, "Already posted this work error in response " + response)

   # def test_user_obo(self):
    def test_post_user_obo(self):
        #Post a work using 3.0 to the record created for testing today
        response = self.post_user_obo(self.version, "work", "ma30_work_user_obo.xml")
        print (response)
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access,'-H', 'Accept: application/xml', '-X', 'GET']
        url = "api." + properties.test_server + "/v3.0/%s/work/" % (self.orcid_id)
        search_pattern = "api." + properties.test_server + r"/v3.0/%s/work/(\d+)" % (self.orcid_id)
        putcode = re.search(search_pattern, re.sub(r'[\s+]', '', response))
        url = "https://" + url + putcode.group(1)
        read_response = self.orcid_curl(url, curl_params)
        assertionTag = re.search("<common:assertion-origin-orcid>(.+?)</common:assertion-origin-orcid>", re.sub(r'[\s+]', '', read_response))
        self.assertTrue(self.orcid_id in assertionTag.group(1), "Response missing \"201\" code: " + response)

