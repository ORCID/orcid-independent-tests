import OrcidBaseTest
import properties
import re

class Api30AllEndPoints(OrcidBaseTest.OrcidBaseTest):

	xml_data_files_path = 'post_files/'

	def setUp(self):
		self.client_id     = properties.memberClientId
		self.client_secret = properties.memberClientSecret
		self.notify_token  = properties.notifyToken
		self.orcid_id    = properties.staticId
		self.access      = properties.staticAccess

#3.0_rc1
	def post20(self, file_name, endpoint):
		curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + file_name, '-X', 'POST']
		post_response = self.orcid_curl("https://api.qa.orcid.org/v3.0_rc1/%s/%s" % (self.orcid_id, endpoint), curl_params)
		return post_response

	def put20(self, putjson, endpoint, putcode):
		curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+json', '-H', 'Accept: application/json', '-d', self.putjson, '-X', 'PUT']
		put_response = self.orcid_curl("https://api.qa.orcid.org/v3.0_rc1/%s/%s/%s" % (self.orcid_id, endpoint, putcode), curl_params)
		return put_response

	def read20(self, endpoint):
		curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
	read_response = self.orcid_curl("https://api.qa.orcid.org/v3.0_rc1/%s/%s" % (self.orcid_id, endpoint), curl_params)
	return read_response

	def delete20(self, endpoint, putcode):
		curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'DELETE']
		delete_response = self.orcid_curl("https://api.qa.orcid.org/v3.0_rc1/%s/%s/%s" % (self.orcid_id, endpoint, putcode), curl_params)
		return delete_response

	def getputcode(self, post_response):
		for header in post_response.split('\n'):
			if("Location:" in header):
				location_chunks = header.split('/')
				putcode = location_chunks[-1].strip()
		return putcode

	def post_group(self, group_access, file_name, endpoint):
		curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + file_name, '-X', 'POST']
		post_response = self.orcid_curl("https://api.qa.orcid.org/v3.0_rc1/%s" % endpoint, curl_params)
		return post_response

	def delete_group(self, endpoint, putcode):
		curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'DELETE']
		delete_response = self.orcid_curl("https://api.qa.orcid.org/v3.0_rc1/%s/%s" % (endpoint, putcode), curl_params)
		return delete_response

	def read_group(self, grou_access, endpoint, putcode):
		curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.group_access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', 'GET']
		read_response = self.orcid_curl("https://api.qa.orcid.org/v3.0_rc1/%s/%s" % (endpoint, putcode), curl_params)
		return read_response

	def group(self, group_access, xmlfile, postendpoint, group_id):
		#Post
		post_response = self.post_group(self.group_access, xmlfile, postendpoint)
		self.assertTrue("201 Created" in post_response, "response: " + post_response)
		#Get put-code
		putcode = self.getputcode(post_response)
		#Read
		read_response = self.read_group(self.group_access, postendpoint, putcode)
		self.assertTrue(group_id in read_response, "response: " + read_response)
		#Delete
		delete_response = self.delete_group(postendpoint, putcode)
		self.assertTrue("204 No Content" in delete_response, "response: " + delete_response)

	def bio20(self, xmlfile, postendpoint, readendpoint, jsontext, postname, putname, manualname):
		#Post
		post_response = self.post20(xmlfile, postendpoint)
		self.assertTrue("201 Created" in post_response, "response: " + post_response)
		#Get put-code
		putcode = self.getputcode(post_response)
		#Update
		self.putjson = '{"put-code":' + str(putcode) + ',' +jsontext
		put_response = self.put20(self.putjson, postendpoint, putcode)
		self.assertTrue("200 OK" in put_response, "response: " + put_response)
		#Read check it was updated
		read_response = self.read20(readendpoint)
		self.assertTrue(putname in read_response and manualname in read_response and postname not in read_response, "response: " + read_response)
		#Delete
		delete_response = self.delete20(postendpoint, putcode)
		self.assertTrue("204 No Content" in delete_response, "response: " + delete_response)
		#Read check it was deleted
		read_response = self.read20(readendpoint)
		self.assertTrue(manualname in read_response and putname not in read_response, "response: " + read_response)

	def works20(self, xmlfile, postendpoint, readendpoint, jsontext, postname, putname, manualname):
		#Post
		post_response = self.post20(xmlfile, postendpoint)
		self.assertTrue("201 Created" in post_response, "response: " + post_response)
		#Read Check for group
		read_response = self.read20(readendpoint)
		self.assertTrue(postname in read_response and '</activities:group><activities:group>' not in re.sub('[\s+]', '', read_response), "response: " + read_response)
		print read_response
		#Get put-code
		putcode = self.getputcode(post_response)
		#Update
		self.putjson = '{"put-code":' + str(putcode) + ',' +jsontext
		put_response = self.put20(self.putjson, postendpoint, putcode)
		self.assertTrue("200 OK" in put_response, "response: " + put_response)
		#Read Check there is no group
		read_response = self.read20(readendpoint)
		self.assertTrue(putname in read_response and '</activities:group><activities:group>' in re.sub('[\s+]', '', read_response), "response: " + read_response)
		print read_response
		#Delete
		delete_response = self.delete20(postendpoint, putcode)
		self.assertTrue("204 No Content" in delete_response, "response: " + delete_response)
		#Read check it was deleted
		read_response = self.read20(readendpoint)
		self.assertTrue(manualname in read_response and putname not in read_response, "response: " + read_response)

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
		self.bio20('30rc1postedu.xml', 'education', 'educations', jsontext, 'Art History', 'Rocket Science', 'Car Repair')

	def test_employ30(self):
		jsontext = '"department-name":"Rocket Science","role-title":"BA","start-date" : {"year" : {"value" : "2001"}},"organization":{"name":"University of Oxford ","address":{"city":"Oxford","region":"Oxfordshire","country":"GB"},"disambiguated-organization" : {"disambiguated-organization-identifier":"6396","disambiguation-source" : "RINGGOLD"}}}'
		self.bio20('30rc1postemploy.xml', 'employment', 'employments', jsontext, 'Annapolis', 'Oxford', 'ORCID')

	def test_distinction30(self):
		jsontext = '"department-name":"Rocket Science","role-title":"BA","start-date" : {"year" : {"value" : "2001"},"month" : {"value" : "07"},"day" : {"value" : "02"}},"organization":{"name":"University of Oxford","address":{"city":"Oxford","region":"Oxfordshire","country":"GB"},"disambiguated-organization" : {"disambiguated-organization-identifier":"grid.4991.5","disambiguation-source" : "GRID"}}}'
		self.bio20('30rc1postdistinct.xml', 'distinction', 'distinctions', jsontext, 'Annapolis', 'Oxford', 'Swarthmore')

	def test_invited30(self):
		jsontext = '"start-date" : {"year" : {"value" : "2001"}},"organization":{"name":"Harvard University","address":{"city":"Cambridge","region":"MA","country":"US"},"disambiguated-organization" : {"disambiguated-organization-identifier":"grid.38142.3c","disambiguation-source" : "GRID"}},"external-ids" : {"external-id" : [ {"external-id-type" : "grant_number","external-id-value" : "external-identifier-value3","external-id-relationship" : "self"}]}}'
		self.bio20('30rc1postinvited.xml', 'invited-position', 'invited-positions', jsontext, 'Digital', 'Harvard', 'Oberlin')

	def test_membership30(self):
		jsontext = '"department-name":"Rocket Science","role-title":"BA","start-date" : {"year" : {"value" : "2001"}},"organization":{"name":"University of Oxford ","address":{"city":"Oxford","region":"Oxfordshire","country":"GB"},"disambiguated-organization" : {"disambiguated-organization-identifier":"6396","disambiguation-source" : "RINGGOLD"}}}'
		self.bio20('30rc1postmembership.xml', 'membership', 'memberships', jsontext, 'Annapolis', 'Oxford', 'AARP')

	def test_qualification30(self):
		jsontext = '"department-name":"Rocket Science","role-title":"BA","start-date" : {"year" : {"value" : "2001"}},"organization":{"name":"University of Oxford ","address":{"city":"Oxford","region":"Oxfordshire","country":"GB"},"disambiguated-organization" : {"disambiguated-organization-identifier":"6396","disambiguation-source" : "RINGGOLD"}}}'
		self.bio20('30rc1postqualify.xml', 'qualification', 'qualifications', jsontext, 'Annapolis', 'Oxford', 'AFL-CIO')

	def test_service30(self):
		jsontext = '"department-name":"Rocket Science","role-title":"BA","start-date" : {"year" : {"value" : "2001"}},"organization":{"name":"University of Oxford","address":{"city":"Oxford","region":"Oxfordshire","country":"GB"},"disambiguated-organization" : {"disambiguated-organization-identifier":"6396","disambiguation-source" : "RINGGOLD"}}}'
		self.bio20('30rc1postservice.xml', 'service', 'services', jsontext, 'Annapolis', 'Oxford', 'ORCID')

	def test_funding30(self):
		jsontext = '"title":{"title":{"value":"Funding to researcher identifiers"}},"external-ids":{"external-id":[{"external-id-type":"grant_number","external-id-value":"7777","external-id-url":null,"external-id-relationship":"self"}]},"type":"grant","organization":{"name":"Wellcome Trust","address":{"city":"London","region":null,"country":"GB"},"disambiguated-organization":{"disambiguated-organization-identifier":"http://dx.doi.org/10.13039/100004440","disambiguation-source":"FUNDREF"}}}'
		self.works20('30rc1postfund.xml', 'funding', 'fundings', jsontext, '6666', '7777', '8888')

	def test_researchresource30(self):
		jsontext = '"proposal":{"title":{"title":{"value":"Special Collections Access Request"}},"hosts":{"organization":[{"name":"Yale University Beinecke Rare Book and Manuscript Library","address":{"city":"New Haven","region":"CT","country":"US"},"disambiguated-organization":{"disambiguated-organization-identifier":"508080","disambiguation-source":"RINGGOLD"}}]},"external-ids":{"external-id":[{"external-id-type":"source-work-id","external-id-value":"1004","external-id-relationship":"self"}]}},"resource-item":[{"resource-name":"Special Collection","resource-type":"collections","hosts":{"organization":[{"name":"Yale University Beinecke Rare Book and Manuscript Library","address":{"city":"New Haven","region":"CT","country":"US"},"disambiguated-organization":{"disambiguated-organization-identifier":"508080","disambiguation-source":"RINGGOLD"}}]},"external-ids":{"external-id":[{"external-id-type":"source-work-id","external-id-value":"1100","external-id-relationship":"self"}]}}]}'
		self.works20('30rc1postrr.xml', 'research-resource', 'research-resources', jsontext, 'Clements', 'Beinecke', 'Laser')

	def test_works20(self):
		jsontext = '"title":{"title":{"value":"Catcher in the Rye"}},"type":"book","external-ids":{"external-id":[{"external-id-type":"doi","external-id-value":"1234","external-id-url":null,"external-id-relationship":"self"}]}}'
		self.works20('20postwork.xml', 'work', 'works', jsontext, 'Great Expectations', 'Catcher in the Rye', 'Harry Potter')

	def test_peerreview_group(self):
		self.group_access = self.orcid_generate_member_token(self.client_id, self.client_secret, "/group-id-record/update")
		self.group(self.group_access, 'group.xml', 'group-id-record', '0000-0005')


 
#read the record: curl -H 'Content-Type: application/orcid+xml' -H 'Authorization: Bearer f4f35385-f903-451c-9a15-cde960dca66b' -X GET 'https://api.qa.orcid.org/v3.0_rc1/0000-0002-7361-1027/fundings' -L -i -k
