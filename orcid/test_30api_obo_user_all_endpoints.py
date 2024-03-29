import OrcidBaseTest
import properties
import re
import local_properties

class Api30AllEndPoints(OrcidBaseTest.OrcidBaseTest):
    
    xml_data_files_path = 'post_files/'

    def setUp(self):
        if properties.type == "actions":
            self.test_server = properties.test_server
            self.client_id = properties.memberClientId
            self.client_secret = properties.memberClientSecret
            self.orcid_id = properties.staticId
            self.access = properties.staticOBOUserAccess
            # 0000-0002-7361-1027
        else:
            self.test_server = local_properties.test_server
            self.orcid_id = local_properties.orcid_id
            self.access = local_properties.step_1_obo_user_access
            self.group_access = local_properties.group_access

#3.0
# The following tests post, get put code, read and check post is in response, then delete for every end-point on the 3.0 API
    def post20(self, file_name, endpoint):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + file_name, '-X', 'POST']
        post_response = self.orcid_curl("https://api." + self.test_server + "/v3.0/%s/%s" % (self.orcid_id, endpoint), curl_params)
        return post_response

    def put20(self, putjson, endpoint, putcode):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+json', '-H', 'Accept: application/json', '-d', self.putjson, '-X', 'PUT']
        put_response = self.orcid_curl("https://api." + self.test_server + "/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), curl_params)
        return put_response

    def read20(self, endpoint):
      curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
      read_response = self.orcid_curl("https://api." + self.test_server + "/v3.0/%s/%s" % (self.orcid_id, endpoint), curl_params)
      return read_response

    def delete20(self, endpoint, putcode):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'DELETE']
        delete_response = self.orcid_curl("https://api." + self.test_server + "/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), curl_params)
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
        post_response = self.orcid_curl("https://api.%s/v3.0/group-id-record/?group-id=%s" % (self.test_server, issn), curl_params)
        self.assertTrue("group-id" in post_response, "response: " + post_response)
        #read
        read_response = self.orcid_curl("https://api.%s/v3.0/group-id-record/1104" % (self.test_server), curl_params)
        self.assertTrue("<group-id:group-id>issn:love</group-id:group-id>" in read_response, "response: " + read_response)
        
    def other_group(self, group_access, xmlfile):
        #post new group
        post_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xmlfile, '-X', 'POST']
        post_response = self.orcid_curl("https://api.%s/v3.0/group-id-record" % (self.test_server), post_params)
        self.assertTrue("HTTP/1.1 201" in post_response, "response: " + post_response)
        #put-code
        putcode = self.getputcode(post_response)
        #read
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', 'GET']
        read_response = self.orcid_curl("https://api.%s/v3.0/group-id-record/%s" % (self.test_server, putcode), curl_params)
        self.assertTrue("<group-id:group-id>orcid-generated:ind</group-id:group-id>" in read_response, "response: " + read_response)
        #delete
        delete_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'DELETE']
        delete_response = self.orcid_curl("https://api.%s/v3.0/group-id-record/%s" % (self.test_server, putcode), delete_params)
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
        #Update
        self.putjson = '{"put-code":' + str(putcode) + ',' +jsontext
        put_response = self.put20(self.putjson, postendpoint, putcode)
        self.assertTrue("HTTP/1.1 200" in put_response, "response: " + put_response)
        #Read Check there is no group
        read_response = self.read20(readendpoint)
        self.assertTrue(putname in read_response and '</activities:group><activities:group>' in re.sub(r'[\s+]', '', read_response), "response: " + read_response)
        print (read_response)
        # Check assertion tag
        assertionTag = re.search("<common:assertion-origin-orcid>(.+?)</common:assertion-origin-orcid>",re.sub(r'[\s+]', '', read_response))
        self.assertTrue(self.orcid_id in assertionTag.group(1), "Response missing \"Created\" tag: " + read_response)
        #Delete
        delete_response = self.delete20(postendpoint, putcode)
        self.assertTrue("HTTP/1.1 204" in delete_response, "response: " + delete_response)
        #Read check it was deleted
        read_response = self.read20(readendpoint)
        self.assertTrue(manualname in read_response and putname not in read_response, "response: " + read_response)

# Each test has josn to put and the parameters are: xml file to post, endpoint to post to, endpoint to read, json to put, text that is in the posted file, text that is in the json put update, manually added text
    def test_othername30(self):
        jsontext = '"display-index":0,"content":"Second Name"}'
        self.bio20('20postname.xml', 'other-names', 'other-names', jsontext, 'First name', 'Second Name', 'Other name')

    def test_country30(self):
        jsontext = '"country":{"value":"CR"}}'
        self.bio20('20postaddress.xml', 'address', 'address', jsontext, 'GB', 'CR', 'US')

    def test_keywords30(self):
        jsontext = '"content":"oranges"}'
        self.bio20('20postkeyword.xml', 'keywords', 'keywords', jsontext, 'apples', 'oranges', 'bananas')

    def test_researcherurls30(self):
        jsontext = '"url-name":"Bing","url":{"value":"www.bing.com"}}'
        self.bio20('20posturl.xml', 'researcher-urls', 'researcher-urls', jsontext, 'Yahoo', 'Bing', 'Google')

    def test_identifiers30(self):
        jsontext = '"external-id-type":"Personal External Identifier","external-id-value":"twenty-nine","external-id-url":{"value":"www.29.com"},"external-id-relationship":"self"}'
        self.bio20('20postid.xml', 'external-identifiers', 'external-identifiers', jsontext, 'A-0003', 'twenty-nine', '1234567')

    def test_education30(self):
        jsontext = '"department-name":"Rocket Science","role-title":"BA","start-date" : {"year" : {"value" : "2000"}},"organization":{"name":"Massachusetts Institute of Technology","address":{"city":"Cambridge","region":"MA","country":"US"},"disambiguated-organization" : {"disambiguated-organization-identifier":"2167","disambiguation-source" : "RINGGOLD"}}}'
        self.bio20('30postedu.xml', 'education', 'educations', jsontext, 'Art History', 'Rocket Science', 'Car Repair')
        
    def test_employ30(self):
        jsontext = '"department-name":"Rocket Science","role-title":"BA","start-date" : {"year" : {"value" : "2001"}},"organization":{"name":"University of Oxford ","address":{"city":"Oxford","region":"Oxfordshire","country":"GB"},"disambiguated-organization" : {"disambiguated-organization-identifier":"6396","disambiguation-source" : "RINGGOLD"}}}'
        self.bio20('30postemploy.xml', 'employment', 'employments', jsontext, 'Annapolis', 'Oxford', 'ORCID')
        
    def test_distinction30(self):
        jsontext = '"department-name":"Rocket Science","role-title":"BA","start-date" : {"year" : {"value" : "2001"},"month" : {"value" : "07"},"day" : {"value" : "02"}},"organization":{"name":"University of Oxford","address":{"city":"Oxford","region":"Oxfordshire","country":"GB"},"disambiguated-organization" : {"disambiguated-organization-identifier":"grid.4991.5","disambiguation-source" : "GRID"}}}'
        self.bio20('30postdistinct.xml', 'distinction', 'distinctions', jsontext, 'Annapolis', 'Oxford', 'Swarthmore')
        
    def test_invited30(self):
        jsontext = '"start-date" : {"year" : {"value" : "2001"}},"organization":{"name":"Harvard University","address":{"city":"Cambridge","region":"MA","country":"US"},"disambiguated-organization" : {"disambiguated-organization-identifier":"grid.38142.3c","disambiguation-source" : "GRID"}},"external-ids" : {"external-id" : [ {"external-id-type" : "grant_number","external-id-value" : "external-identifier-value3","external-id-relationship" : "self"}]}}'
        self.bio20('30postinvited.xml', 'invited-position', 'invited-positions', jsontext, 'Digital', 'Harvard', 'Oberlin')
        
    def test_membership30(self):
        jsontext = '"department-name":"Rocket Science","role-title":"BA","start-date" : {"year" : {"value" : "2001"}},"organization":{"name":"University of Oxford ","address":{"city":"Oxford","region":"Oxfordshire","country":"GB"},"disambiguated-organization" : {"disambiguated-organization-identifier":"6396","disambiguation-source" : "RINGGOLD"}}}'
        self.bio20('30postmembership.xml', 'membership', 'memberships', jsontext, 'Annapolis', 'Oxford', 'AARP')
        
    def test_qualification30(self):
        jsontext = '"department-name":"Rocket Science","role-title":"BA","start-date" : {"year" : {"value" : "2001"}},"organization":{"name":"University of Oxford ","address":{"city":"Oxford","region":"Oxfordshire","country":"GB"},"disambiguated-organization" : {"disambiguated-organization-identifier":"6396","disambiguation-source" : "RINGGOLD"}}}'
        self.bio20('30postqualify.xml', 'qualification', 'qualifications', jsontext, 'Annapolis', 'Oxford', 'AFL-CIO')
        
    def test_service30(self):
        jsontext = '"department-name":"Rocket Science","role-title":"BA","start-date" : {"year" : {"value" : "2001"}},"organization":{"name":"University of Oxford","address":{"city":"Oxford","region":"Oxfordshire","country":"GB"},"disambiguated-organization" : {"disambiguated-organization-identifier":"6396","disambiguation-source" : "RINGGOLD"}}}'
        self.bio20('30postservice.xml', 'service', 'services', jsontext, 'Annapolis', 'Oxford', 'ORCID')

    def test_funding30(self):
        jsontext = '"title":{"title":{"value":"Funding to researcher identifiers"}},"external-ids":{"external-id":[{"external-id-type":"grant_number","external-id-value":"7777","external-id-url":null,"external-id-relationship":"self"}]},"type":"grant","organization":{"name":"Wellcome Trust","address":{"city":"London","region":null,"country":"GB"},"disambiguated-organization":{"disambiguated-organization-identifier":"http://dx.doi.org/10.13039/100004440","disambiguation-source":"FUNDREF"}}}'
        self.works20('30postfund.xml', 'funding', 'fundings', jsontext, '6666', '7777', '8888')

    def test_researchresource30(self):
        jsontext = '"proposal":{"title":{"title":{"value":"Special Collections Access Request"}},"hosts":{"organization":[{"name":"Yale University Beinecke Rare Book and Manuscript Library","address":{"city":"New Haven","region":"CT","country":"US"},"disambiguated-organization":{"disambiguated-organization-identifier":"508080","disambiguation-source":"RINGGOLD"}}]},"external-ids":{"external-id":[{"external-id-type":"source-work-id","external-id-value":"1004","external-id-relationship":"self"}]}},"resource-item":[{"resource-name":"Special Collection","resource-type":"collections","hosts":{"organization":[{"name":"Yale University Beinecke Rare Book and Manuscript Library","address":{"city":"New Haven","region":"CT","country":"US"},"disambiguated-organization":{"disambiguated-organization-identifier":"508080","disambiguation-source":"RINGGOLD"}}]},"external-ids":{"external-id":[{"external-id-type":"source-work-id","external-id-value":"1100","external-id-relationship":"self"}]}}]}'
        self.works20('30postrr.xml', 'research-resource', 'research-resources', jsontext, 'Clements', 'Beinecke', 'Laser')

    def test_works30(self):
        jsontext = '"title":{"title":{"value":"Catcher in the Rye"}},"type":"book","external-ids":{"external-id":[{"external-id-type":"doi","external-id-value":"1234","external-id-url":null,"external-id-relationship":"self"}]}}'
        self.works20('20postwork.xml', 'work', 'works', jsontext, 'Great Expectations', 'Catcher in the Rye', 'Harry Potter')     
    
    def test_peer20(self):
        jsontext = '"reviewer-role" : "reviewer", "review-identifiers" : { "external-id" : [ {"external-id-type" : "source-work-id","external-id-value" : "6666", "external-id-url" : null,"external-id-relationship" : "self"} ] }, "review-url" : null, "review-type" : "review", "review-completion-date" : { "year" : { "value" : "2006" }}, "review-group-id" : "issn:1741-4857", "convening-organization" : { "name" : "Crossref", "address" : { "city" : "Lynnfield", "region" : "MA", "country" : "US" }, "disambiguated-organization" : {"disambiguated-organization-identifier" : "grid.466633.2", "disambiguation-source" : "GRID" }}}'
        self.bio20('30postpeer.xml', 'peer-review', 'peer-reviews', jsontext, '5555', '6666', '13')

    def test_client_endpoint(self):
        #check response of the client endpoint
        curl_params = ['-i', '-L', '-k', '-H', "Accept: application/json"]
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0/client/APP-7M3CGDKMQE36J56N", curl_params)
        self.assertTrue("secret" not in response, "Unexpected response: " + response)
        
    def test_client_endpoint(self):
        #check response of the client endpoint in xml
        curl_params = ['-i', '-L', '-k', '-H', "Accept: application/vnd.orcid+xml"]
        response = self.orcid_curl("https://pub." + self.test_server + "/v3.0/client/APP-7M3CGDKMQE36J56N", curl_params)
        self.assertTrue("secret" not in response, "Unexpected response: " + response)
