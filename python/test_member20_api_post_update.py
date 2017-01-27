import OrcidBaseTest
import pyjavaproperties

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):
    
    xml_data_files_path = '../ORCID-Source/orcid-integration-test/src/test/manual-test/'

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test-client.properties'))
        self.orcid_props   = p
        self.client_id     = self.orcid_props['memberClientId']
        self.client_secret = self.orcid_props['memberClientSecret']        
        self.code          = self.orcid_props['api2PostUpdateCode']
        self.orcid_id      = self.orcid_props['orcidId']
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
    '''
    def test_blank(self):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml']
        response = self.orcid_curl("", curl_params)
        self.assertTrue("201 Created" in response, "response: " + response)
    '''

    def test_post_work(self):
        # TEST 85 Post the ma test work 2
        self.assertIsNotNone(self.access,"Bearer not recovered: " + str(self.access))
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + 'ma2_work.xml', '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v2.0_rc3/%s/work" % self.orcid_id, curl_params)
        self.assertTrue("201 Created" in response, "Response missing \"Created\" tag: " + response)
        putcode = self.get_putcode_from_response(response)
        self.assertIsNotNone(putcode,"Not valid putcode returned: [%s]" % str(putcode))
        # TEST 88 Update the work with JSON
        self.assertFalse("" == putcode, "Empty putcode in url")
        updated_data = "'{\"put-code\":\"%d\",\"title\":{\"title\":\"APITestTitleUpdated\"},\"type\":\"JOURNAL_ARTICLE\",\"external-ids\":{\"external-id\":[{\"external-id-value\":\"1234\",\"external-id-type\":\"doi\",\"external-id-relationship\":\"SELF\"}]}}'" % int(putcode)
        update_curl_params = ['-i', '-L', '-k', '-H', 'Authorization: Bearer ' + str(self.access), '-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-d', updated_data, '-X', 'PUT']
        update_response = self.orcid_curl("https://api.qa.orcid.org/v2.0_rc3/%s/work/%d" % (self.orcid_id,int(putcode)), update_curl_params)
        self.assertTrue("PRINT" in update_response, str(putcode) + " > Update Action Response: " + update_response + " with data [%s]" % updated_data)
        # TEST 90 Delete the work


#curl -H 'Content-Type: application/orcid+json' -H 'Authorization: Bearer b5571b26-d171-45fb-b868-7256ed220de0' -H 'Accept: application/json' -d '{"put-code":"155510","title": {"title": "API Test Title Updated"},"type": "JOURNAL_ARTICLE","external-ids": {"external-id": [{"external-id-value": "1234","external-id-type": "doi","external-id-relationship": "SELF"}]} }' -X PUT 'https://api.qa.orcid.org/v2.0_rc3/0000-0003-4248-6064/work/155510'        
'''

curl -H 'Content-Type: application/orcid+json' -H 'Authorization: Bearer b5571b26-d171-45fb-b868-7256ed220de0' -H 'Accept: application/json' -d '{"put-code":"155510","title": {"title": "API Test Title Updated"},"type": "JOURNAL_ARTICLE","external-ids": {"external-id": [{"external-id-value": "1234","external-id-type": "doi","external-id-relationship": "SELF"}]} }' -X PUT 'https://api.qa.orcid.org/v2.0_rc3/0000-0003-4248-6064/work/155510'

90. Delete the work:
 
    ```
    curl -H 'Content-Type: application/orcid+xml' -H 'Authorization: Bearer [2.0 token]' -H 'Accept: application/xml' -X DELETE 'https://api.qa.orcid.org/v2.0_rc3/[orcid id]/work/[put-code]' -L -i -k
    ```
91. Check that the work is no longer listed at https://qa.orcid.org/my-orcid

92. Post an education item:
 
    ```
    curl -H 'Content-Type: application/orcid+xml' -H 'Authorization: Bearer [2.0 token]' -H 'Accept: application/xml' -d '@ma2_edu.xml' -X POST 'https://api.qa.orcid.org/v2.0_rc3/[orcid id]/education' -L -i -k
    ```

93. Post a funding item:
 
    ```
    curl -H 'Content-Type: application/orcid+xml' -H 'Authorization: Bearer [2.0 token]' -H 'Accept: application/xml' -d '@ma2_fund2.xml' -X POST 'https://api.qa.orcid.org/v2.0_rc3/[orcid id]/funding' -L -i -k
    ```

94. Post a peer-review item:
 
    ```
    curl -H 'Content-Type: application/orcid+xml' -H 'Authorization: Bearer [2.0 token]' -H 'Accept: application/xml' -d '@ma2_peer2.xml' -X POST 'https://api.qa.orcid.org/v2.0_rc3/[orcid id]/peer-review' -L -i -k
    ```

95. Check that the education, funding and peer-review item appear at https://qa.orcid.org/my-orcid
    
96. Post a keyword:
    ```
    curl -H 'Content-Type: application/orcid+xml' -H 'Authorization: Bearer [2.0 token]' -H 'Accept: application/xml' -d '@ma2_keyword.xml' -X POST 'https://api.qa.orcid.org/v2.0_rc3/[orcid id]/keywords' -L -i -k
    ```

97. Post a personal external identifier:
    ```
    curl -H 'Content-Type: application/orcid+xml' -H 'Authorization: Bearer [2.0 token]' -H 'Accept: application/xml' -d '@ma2_identifier.xml' -X POST 'https://api.qa.orcid.org/v2.0_rc3/[orcid id]/external-identifiers' -L -i -k
    ```
98. Check that the keyword and external identifier appear at https://qa.orcid.org/my-orcid and no other personal information was changed

99. Post a notification

    ```
    curl -i -H 'Authorization: Bearer eafafe49-b5bf-41db-9fb5-ad3a6cba575b' -H 'Content-Type: application/orcid+xml' -X POST -d '@notify.xml' https://api.qa.orcid.org/v2.0_rc3/[orcid id]/notification-permission -k
    ```
    
100. Go to https://qa.orcid.org/inbox

* Check that notification to add a work has posted
* Check that notifications from the previous updates have posted

'''
'''
{
    'put-code':'155506',
    'title': {
        'title': 'API Test Title Updated'
    },
    'type': 'JOURNAL_ARTICLE',
    'external-ids': {
        'external-id': [
            {
                'external-id-value': '1234',
                'external-id-type': 'doi',
                'external-id-relationship': 'SELF'
            }
        ]
    }
}}


{'put-code':'155507','title': {'title': 'API Test Title Updated'},'type': 'JOURNAL_ARTICLE','external-ids': {'external-id': [{'external-id-value': '1234','external-id-type': 'doi','external-id-relationship': 'SELF'}]}}






{
    "put-code":"155511",
    "title": {"title": "API Test Title Updated"},
    "type": "JOURNAL_ARTICLE",
    "external-ids": {
        "external-id": [
            {"external-id-value": "1234","external-id-type": "doi","external-id-relationship": "SELF"}
        ]
    }
}





'''