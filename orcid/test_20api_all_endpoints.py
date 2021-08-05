import OrcidBaseTest
import properties
import re
import local_properties

class Api20AllEndPoints(OrcidBaseTest.OrcidBaseTest):
    
    xml_data_files_path = 'post_files/'

    def setUp(self):
        # 0000-0002-7361-1027
        if properties.type == "actions":
          self.client_id = properties.memberClientId
          self.client_secret = properties.memberClientSecret
          self.notify_token = properties.notifyToken
          self.orcid_id = properties.staticId
          self.access = properties.staticAccess
          self.group_access = self.orcid_generate_member_token(self.client_id, self.client_secret,"/group-id-record/update")
        else:
          self.orcid_id = local_properties.orcid_id
          self.access = local_properties.step_1_access
          self.group_access = local_properties.group_access

#2.0
    def post20(self, file_name, endpoint):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + file_name, '-X', 'POST']
        post_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s" % (self.orcid_id, endpoint), curl_params)
        return post_response

    def put20(self, putjson, endpoint, putcode):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+json', '-H', 'Accept: application/json', '-d', self.putjson, '-X', 'PUT']
        put_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), curl_params)
        return put_response

    def read20(self, endpoint):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
        read_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s" % (self.orcid_id, endpoint), curl_params)
        return read_response

    def delete20(self, endpoint, putcode):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'DELETE']
        delete_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), curl_params)
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
        post_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/group-id-record/?group-id=%s" % (issn), curl_params)
        self.assertTrue("group-id" in post_response, "response: " + post_response)
        #read
        read_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/group-id-record/1104", curl_params)
        self.assertTrue("<group-id:group-id>issn:love</group-id:group-id>" in read_response, "response: " + read_response)
        
    def other_group(self, group_access, xmlfile):
        #post new group
        post_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + xmlfile, '-X', 'POST']
        post_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/group-id-record", post_params)
        self.assertTrue("HTTP/1.1 201" in post_response, "response: " + post_response)
        #put-code
        putcode = self.getputcode(post_response)
        #read
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', 'GET']
        read_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/group-id-record/%s" %(putcode), curl_params)
        self.assertTrue("<group-id:group-id>orcid-generated:ind</group-id:group-id>" in read_response, "response: " + read_response)
        #delete
        delete_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'DELETE']
        delete_response = self.orcid_curl("https://api.qa.orcid.org/v2.0/group-id-record/%s" % (putcode), delete_params)
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

    def test_country20(self):
        jsontext = '"country":{"value":"CR"}}'
        self.bio20('20postaddress.xml', 'address', 'address', jsontext, 'GB', 'CR', 'US')

    def test_keywords20(self):
        jsontext = '"content":"oranges"}'
        self.bio20('20postkeyword.xml', 'keywords', 'keywords', jsontext, 'apples', 'oranges', 'bananas')

    def test_researcherurls20(self):
        jsontext = '"url-name":"Bing","url":{"value":"www.bing.com"}}'
        self.bio20('20posturl.xml', 'researcher-urls', 'researcher-urls', jsontext, 'Yahoo', 'Bing', 'Google')

    def test_identifiers20(self):
        jsontext = '"external-id-type":"Personal External Identifier","external-id-value":"twenty-nine","external-id-url":{"value":"www.29.com"},"external-id-relationship":"SELF"}'
        self.bio20('20postid.xml', 'external-identifiers', 'external-identifiers', jsontext, 'A-0003', 'twenty-nine', '1234567')

    def test_education20(self):
        jsontext = '"department-name":"Rocket Science","role-title":"BA","organization":{"name":"Massachusetts Institute of Technology","address":{"city":"Cambridge","region":"MA","country":"US"},"disambiguated-organization" : {"disambiguated-organization-identifier":"2167","disambiguation-source" : "RINGGOLD"}}}'
        self.bio20('20postedu.xml', 'education', 'educations', jsontext, 'Art History', 'Rocket Science', 'Car Repair')

    def test_employment20(self):
        jsontext = '"organization":{"name":"University of Oxford ","address":{"city":"Oxford","region":"Oxfordshire","country":"GB"},"disambiguated-organization" : {"disambiguated-organization-identifier":"6396","disambiguation-source" : "RINGGOLD"}}}'
        self.bio20('20postemploy.xml', 'employment', 'employments', jsontext, 'Annapolis', 'Oxford', 'ORCID')

    def test_funding20(self):
        jsontext = '"title":{"title":{"value":"Funding to researcher identifiers"}},"external-ids":{"external-id":[{"external-id-type":"grant_number","external-id-value":"7777","external-id-url":null,"external-id-relationship":"SELF"}]},"type":"GRANT","organization":{"name":"Wellcome Trust","address":{"city":"London","region":null,"country":"GB"},"disambiguated-organization":{"disambiguated-organization-identifier":"http://dx.doi.org/10.13039/100004440","disambiguation-source":"FUNDREF"}}}'
        self.works20('20postfund.xml', 'funding', 'fundings', jsontext, '6666', '7777', '8888')

    def test_works20(self):
        jsontext = '"title":{"title":{"value":"Catcher in the Rye"}},"type":"BOOK","external-ids":{"external-id":[{"external-id-type":"doi","external-id-value":"1234","external-id-url":null,"external-id-relationship":"SELF"}]}}'
        self.works20('20postwork.xml', 'work', 'works', jsontext, 'Great Expectations', 'Catcher in the Rye', 'Harry Potter')
        
    def test_peer20(self):
        jsontext = '"reviewer-role" : "REVIEWER", "review-identifiers" : { "external-id" : [ {"external-id-type" : "source-work-id","external-id-value" : "6666", "external-id-url" : null,"external-id-relationship" : "SELF"} ] }, "review-url" : null, "review-type" : "REVIEW", "review-completion-date" : { "year" : { "value" : "2006" }}, "review-group-id" : "issn:0953-1513", "convening-organization" : { "name" : "ORCID", "address" : { "city" : "Bethesda", "region" : "MD", "country" : "US" }, "disambiguated-organization" : {"disambiguated-organization-identifier" : "385488", "disambiguation-source" : "RINGGOLD" }}}'
        self.bio20('20postpeer.xml', 'peer-review', 'peer-reviews', jsontext, '5555', '6666', '13')

    def test_peerreview_group(self):
    #search for and read a peer-review group with an issn group id
        self.issn_group(self.group_access, '1741-4857')
        
    def test_other_group(self):
    #create, read, delete a peer-review group with a non issn group id
        self.other_group(self.group_access, 'group.xml')