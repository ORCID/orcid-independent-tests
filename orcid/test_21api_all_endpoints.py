import OrcidBaseTest
import properties
import re
import local_properties

class Api20AllEndPoints(OrcidBaseTest.OrcidBaseTest):
    
    xml_data_files_path = 'post_files/'

    def setUp(self):
        # 0000-0002-7361-1027
        if properties.type == "actions":
          self.test_server = properties.test_server
          self.client_id     = properties.memberClientId
          self.client_secret = properties.memberClientSecret
          self.notify_token  = properties.notifyToken
          self.orcid_id    = properties.staticId
          self.access      = properties.staticAccess
          self.group_access = self.orcid_generate_member_token(self.client_id, self.client_secret, "/group-id-record/update")
        else:
          self.test_server = local_properties.test_server
          self.orcid_id    = local_properties.orcid_id
          self.access      = local_properties.step_1_access
          self.group_access = local_properties.group_access

#2.0
    def post20(self, file_name, endpoint):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + file_name, '-X', 'POST']
        post_response = self.orcid_curl("https://api.%s/v2.1/%s/%s" % (self.test_server, self.orcid_id, endpoint), curl_params)
        return post_response

    def put20(self, putjson, endpoint, putcode):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+json', '-H', 'Accept: application/json', '-d', self.putjson, '-X', 'PUT']
        put_response = self.orcid_curl("https://api.%s/v2.1/%s/%s/%s" % (self.test_server, self.orcid_id, endpoint, putcode), curl_params)
        return put_response

    def read20(self, endpoint):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
        read_response = self.orcid_curl("https://api.%s/v2.1/%s/%s" % (self.test_server, self.orcid_id, endpoint), curl_params)
        return read_response

    def delete20(self, endpoint, putcode):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'DELETE']
        delete_response = self.orcid_curl("https://api.%s/v2.1/%s/%s/%s" % (self.test_server, self.orcid_id, endpoint, putcode), curl_params)
        return delete_response

    def getputcode(self, post_response):
        for header in post_response.split('\n'):
            if("Location:" in header):
                location_chunks = header.split('/')
                putcode = location_chunks[-1].strip()
        return putcode


    def issn_group(self, group_access, issn):
        #search
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
        post_response = self.orcid_curl("https://api.%s/v2.1/group-id-record/?group-id=%s" % (self.test_server, issn), curl_params)
        self.assertTrue("group-id" in post_response, "response: " + post_response)
        #read
        read_response = self.orcid_curl("https://api.%s/v2.1/group-id-record/1104" % (self.test_server), curl_params)
        self.assertTrue("<group-id:group-id>issn:love</group-id:group-id>" in read_response, "response: " + read_response)

    def other_group(self, group_access, xmlfile):
        #post new group
        post_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xmlfile, '-X', 'POST']
        post_response = self.orcid_curl("https://api.%s/v2.1/group-id-record" % (self.test_server), post_params)
        self.assertTrue("HTTP/1.1 201" in post_response, "response: " + post_response)
        #put-code
        putcode = self.getputcode(post_response)
        #read
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', 'GET']
        read_response = self.orcid_curl("https://api.%s/v2.1/group-id-record/%s" % (self.test_server, putcode), curl_params)
        self.assertTrue("<group-id:group-id>orcid-generated:ind</group-id:group-id>" in read_response, "response: " + read_response)
        #delete
        delete_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'DELETE']
        delete_response = self.orcid_curl("https://api.%s/v2.1/group-id-record/%s" % (self.test_server, putcode), delete_params)
        self.assertTrue("HTTP/1.1 204" in delete_response, "response: " + delete_response)

    def bio20(self, xmlfile, postendpoint, readendpoint, jsontext, postname, putname, manualname):
        #Post
        post_response = self.post20(xmlfile, postendpoint)
        self.assertTrue("HTTP/1.1 201" in post_response, "response: " + post_response)
        #Get put-code
        putcode = self.getputcode(post_response)
        #Update
        self.putjson = '{"put-code":' + str(putcode) + ',' +jsontext
        put_response = self.put20(self.putjson, postendpoint, putcode)
        self.assertTrue("HTTP/1.1 200" in put_response, "response: " + put_response)
        #Read check it was updated
        read_response = self.read20(readendpoint)
        self.assertTrue(putname in read_response and manualname in read_response and postname not in read_response, "response: " + read_response)
        #Delete
        delete_response = self.delete20(postendpoint, putcode)
        self.assertTrue("HTTP/1.1 204" in delete_response, "response: " + delete_response)
        #Read check it was deleted
        read_response = self.read20(readendpoint)
        self.assertTrue(manualname in read_response and putname not in read_response, "response: " + read_response)

    def works20(self, xmlfile, postendpoint, readendpoint, jsontext, postname, putname, manualname):
        #Post
        post_response = self.post20(xmlfile, postendpoint)
        self.assertTrue("HTTP/1.1 201" in post_response, "response: " + post_response)
        #Read Check for group
        read_response = self.read20(readendpoint)
        self.assertTrue(postname in read_response and '</activities:group><activities:group>' not in re.sub(r'[\s+]', '', read_response), "response: " + read_response)
        print (read_response)
        #Get put-code
        putcode = self.getputcode(post_response)
        # Check creation date after posting the item
        search_pattern = "%s(.+?)</common:created-date>" % putcode
        creation_date_post = re.search(search_pattern, re.sub(r'[\s+]', '', read_response))
        creation_date_post = creation_date_post.group(1)
        creation_date_post = creation_date_post.split('<common:created-date>')[1]
        #Update
        self.putjson = '{"put-code":' + str(putcode) + ',' +jsontext
        put_response = self.put20(self.putjson, postendpoint, putcode)
        self.assertTrue("HTTP/1.1 200" in put_response, "response: " + put_response)
        #Read Check there is no group
        read_response = self.read20(readendpoint)
        # Check creation date after updating the item
        creation_date_put = re.search(search_pattern, re.sub(r'[\s+]', '', read_response))
        creation_date_put = creation_date_put.group(1)
        creation_date_put = creation_date_put.split('<common:created-date>')[1]
        self.assertTrue(putname in read_response and '</activities:group><activities:group>' in re.sub(r'[\s+]', '', read_response), "response: " + read_response)
        self.assertTrue(creation_date_put == creation_date_post, "post: " + creation_date_post + "; put: " + creation_date_put)
        print (read_response)
        #Delete
        delete_response = self.delete20(postendpoint, putcode)
        self.assertTrue("HTTP/1.1 204" in delete_response, "response: " + delete_response)
        #Read check it was deleted
        read_response = self.read20(readendpoint)
        self.assertTrue(manualname in read_response and putname not in read_response, "response: " + read_response)

    def test_othername20(self):
        jsontext = '"display-index":0,"content":"Second Name"}'
        self.bio20('20postname.xml', 'other-names', 'other-names', jsontext, 'First name', 'Second Name', 'Other name')

    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_1/crud_address_v21.cy.js

    def test_keywords20(self):
        jsontext = '"content":"oranges"}'
        self.bio20('20postkeyword.xml', 'keywords', 'keywords', jsontext, 'apples', 'oranges', 'bananas')

    def test_researcherurls20(self):
        jsontext = '"url-name":"Bing","url":{"value":"www.bing.com"}}'
        self.bio20('20posturl.xml', 'researcher-urls', 'researcher-urls', jsontext, 'Yahoo', 'Bing', 'Google')

    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_1/crud_externalids_v21.cy.js
    
    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_1/crud_education_v21.cy.js

    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_1/crud_employment_v21.cy.js

    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_1/crud_funding_v21.cy.js

    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_1/crud_work_v21.cy.js
    
    # Removed, covered here: https://github.com/ORCID/orcid-cypress_tests-private/blob/main/cypress/e2e/mapi/v2_1/crud_peerReview_v21.cy.js

    def test_peerreview_group(self):
        #search for and read a peer-review group with an issn group id
        self.issn_group(self.group_access, '1741-4857')
        
    def test_other_group(self):
        #create, read, delete a peer-review group with a non issn group id
        self.other_group(self.group_access, 'group.xml')