import OrcidBaseTest
import properties
import local_properties

class ExpectedErrors(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.scope                  = "/read-limited%20/activities/update%20/person/update"
        self.wrong_orcid_id         = '0000-0002-2619-0514'   
        self.invalid_id             = '0000-0000-0000-0000'     
        if properties.type == "actions":
            self.test_server = properties.test_server
            self.static_orcid_id = properties.staticId
            self.static_access = properties.staticAccess
            self.orcid_id      = properties.orcidId
            self.client_id     = properties.memberClientId
            self.client_secret = properties.memberClientSecret
            self.member_client_id     = properties.premiumClientId
            self.member_client_secret = properties.premiumClientSecret
            
        else:
            self.test_server = local_properties.test_server
            self.static_orcid_id = local_properties.orcid_id
            self.static_access = local_properties.step_1_access
            self.orcid_id = local_properties.orcid_id_member            
            self.client_id = local_properties.step_2_client_id
            self.client_secret = local_properties.step_2_client_secret
            self.member_client_id = local_properties.premiumClientId
            self.member_client_secret = local_properties.premiumClientSecret

        self.code                   = self.generate_auth_code(self.client_id, self.scope)        
        self.access,self.refresh    = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
        self.scope2                 = "/orcid-bio/update%20/orcid-works/create%20/orcid-works/update%20/affiliations/create%20/affiliations/update%20/funding/create%20/funding/update%20/orcid-profile/read-limited"
        self.code2                  = self.generate_auth_code(self.member_client_id, self.scope2)
        self.access2,self.refresh2  = self.orcid_exchange_auth_token(self.member_client_id, self.member_client_secret, self.code2)
        
		
        #This batch of tests check to see if the API throws expected errors for incorrect actions
    def test_access_wrong_record2(self):
        # Test that posting a work to the wrong orcid record with the 2.0 API returns the expected 401 unauthorized error
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma2_work.xml', '-L', '-i', '-k', '-X', 'POST']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.wrong_orcid_id + "/work", curl_params)
        self.assertTrue("HTTP/1.1 401" in response, "Non 401 returned: " + response)

    def test_access_wrong_record21(self):
        # Test that posting a work to the wrong orcid record with the 2.1 API returns the expected 401 unauthorized error
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma21_work.xml', '-L', '-i', '-k', '-X', 'POST']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.wrong_orcid_id + "/work", curl_params)
        self.assertTrue("HTTP/1.1 401" in response, "Non 401 returned: " + response)

    def test_access_wrong_record30rc1(self):
        # Post a work using an access token for another record using the 3.0_rc1 API
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma30_work.xml', '-L', '-i', '-k', '-X', 'POST']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.wrong_orcid_id + "/work", curl_params)
        self.assertTrue("HTTP/1.1 401" in response, "Non 401 returned: " + response)

    def test_access_record2_without_token(self):
        # Test posting a work using 2.0 API without using a token returns the expected 403 forbidden error
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma2_work.xml', '-L', '-i', '-k', '-X', 'POST']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.orcid_id + "/work", curl_params)
        self.assertTrue("HTTP/1.1 403" in response, "Non 401 returned: " + response)

    def test_access_record21_without_token(self):
        # Test posting a work using 2.1 API without using a token returns the expected 403 forbidden error
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma21_work.xml', '-L', '-i', '-k', '-X', 'POST']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.orcid_id + "/work", curl_params)
        self.assertTrue("HTTP/1.1 403" in response, "Non 401 returned: " + response)

    def test_access_record30rc1_without_token(self):
        # Test posting the ma30_work.xml work using 3.0_rc1 API without using a token returns the expected 403 forbidden error
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma30_work.xml', '-L', '-i', '-k', '-X', 'POST']
        response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.orcid_id + "/work", curl_params)
        self.assertTrue("HTTP/1.1 403" in response, "Non 401 returned: " + response)

    def test_update_record2_without_token(self):
        # Post the ma test work 2 using the basic client
        response = self.post_activity("/v2.0/", "work", "ma2_work.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"201\" code: " + response)
        putcode = str(self.get_putcode_from_response(response)).strip()
        self.assertIsNotNone(putcode,"No valid putcode returned: [%s]" % str(putcode))
        # Update the work with JSON
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = "{'put-code':'%s','title':{'title':'APITestTitleUpdated'},'type':'JOURNAL_ARTICLE','external-ids':{'external-id':[{'external-id-value':'123456','external-id-type':'doi','external-id-relationship':'SELF'}]}}" %  str(putcode)
        activity_type = "work"
        update_curl_params = ['-i', '-L', '-k', '-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-d', updated_data, '-X', 'PUT']
        update_response = self.orcid_curl("https://api." + self.test_server + "/v2.0/%s/%s/%d" % (self.orcid_id, activity_type, int(putcode)), update_curl_params)
        self.assertTrue("HTTP/1.1 403" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
        # Delete the work
        delete_response = self.delete_activity("/v2.0/", putcode, "work")
        self.assertTrue("HTTP/1.1 204" in delete_response, "Delete Action Response: " + delete_response + " using putcode [%s]" % str(putcode))

    def test_update_record2_from_other_source(self):
        # Post the ma test work 2 using the basic client
        response = self.post_activity("/v2.0/", "work", "ma2_work.xml")
        self.assertTrue("HTTP/1.1 201" in response, "Response missing \"201\" code: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"No valid putcode returned: [%s]" % str(putcode))
        # TEST 116 Attempt to update the work using the premium client with old scopes
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = '{"put-code":' + str(putcode).strip() + ',"title":{"title":"APITestTitleUpdated"},"type":"JOURNAL_ARTICLE","external-ids":{"external-id":[{"external-id-value":"12345","external-id-type":"doi","external-id-relationship":"SELF"}]}}'
        update_curl_params = ['-i', '-L', '-k', '-H', 'Authorization: Bearer ' + str(self.access2), '-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-d', updated_data, '-X', 'PUT']
        update_response = self.orcid_curl("https://api." + self.test_server + "/v2.0/%s/%s/%s" % (self.orcid_id, "work", str(putcode).strip()), update_curl_params)
        self.assertTrue("HTTP/1.1 403" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
        # Delete the work
        delete_response = self.delete_activity("/v2.0/", putcode, "work")
        self.assertTrue("HTTP/1.1 204" in delete_response, "Delete Action Response: " + delete_response + " using putcode [%s]" % str(putcode))

    def test_member_http_read_20(self):
        #Test making a call with 2.0 API using http not https returns the expected '521 Origin Down' error
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.static_access, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("http://pub." + properties.test_server + "/v2.0/" + self.static_orcid_id + "/record", curl_params)
        codeStart = response.find("HTTP/1.1 ")
        codeEnd = codeStart + 12
        self.assertTrue(response[codeStart:codeEnd].strip() in ["HTTP/1.1 521", "HTTP/1.1 400"], "Expected error code '521' or '400', instead: " + response)

    def test_member_http_read_21(self):
        #Test making a call with 2.0 API using http not https returns the expected '521 Origin Down' error
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.static_access, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("http://pub." + properties.test_server + "/v2.1/" + self.static_orcid_id + "/record", curl_params)
        codeStart = response.find("HTTP/1.1 ")
        codeEnd = codeStart + 12
        self.assertTrue(response[codeStart:codeEnd].strip() in ["HTTP/1.1 521", "HTTP/1.1 400"], "Expected error code '521' or '400', instead: " + response)

    def test_nonexisting_record(self):
        #Confirm that the response type is 404 when fetching a non-existing record
        curl_params = ['-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml','-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://%s/%s" % (self.test_server, self.invalid_id), curl_params)
        self.assertTrue("HTTP/1.1 404" in response, "Non 404 returned: " + response)