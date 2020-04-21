import OrcidBaseTest
import properties
import local_properties

class ReadEndPoints(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
    	self.public_orcid_id    = '0000-0002-3874-7658'
        self.pubapi_public_token= 'a8ac4d85-df2b-4de2-9411-1b94491f463b'
        self.memapi_public_token= 'eba7892b-4f4a-4651-9c47-f0c74fae61c5'
        self.limited_orcid_id = '0000-0001-7325-5491'
        self.limited_token = '1fcda8a0-1af3-4b35-8825-e4c53dae8953'
        self.sections = ['', 'record', 'activities', 'address', 'biography', 'distinctions', 'educations', 'employments', 'external-identifiers', 'fundings', 'invited-positions', 'keywords', 'memberships', 'other-names', 'peer-reviews', 'person', 'personal-details', 'qualifications', 'research-resources', 'researcher-urls', 'services', 'works']
        self.limited_items = ['address/1070', 'distinction/4992', 'education/4978', 'employment/4979', 'external-identifiers/302', 'funding/1285', 'invited-position/4991', 'keywords/1280', 'other-names/2686', 'peer-review/1077', 'qualification/4990', 'research-resource/1005', 'researcher-urls/7187', 'service/4663', 'work/141942', 'works/141942']
        self.limited_summaries = ['distinction/summary/4992', 'education/summary/4978', 'employment/summary/4979', 'funding/summary/1285', 'invited-position/summary/4991', 'peer-review/summary/1077', 'qualification/summary/4990', 'research-resource/summary/1005', 'service/summary/4663', 'work/summary/141942']
        self.public_items = ['address/1069', 'education/1409', 'employment/1410', 'external-identifiers/250', 'funding/1284', 'invited-position/4667', 'keywords/1278', 'membership/4670', 'other-names/2685', 'peer-review/1076', 'qualification/4666', 'research-resource/1006', 'researcher-urls/7186', 'service/4669', 'work/141941', 'works/141941']
        self.public_summaries = ['education/summary/1409', 'employment/summary/1410', 'funding/summary/1284', 'invited-position/summary/4667', 'membership/summary/4670', 'peer-review/summary/1076', 'qualification/summary/4666', 'research-resource/summary/1006', 'service/summary/4669', 'work/summary/141941']
        if local_properties.type == "jenkins":
          self.test_server = properties.test_server
        else:
          self.test_server = local_properties.test_server

        
    def read_members(self, version, orcid_id, token, endpoint):
    	curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + token, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
    	read_response = self.orcid_curl("https://api." + self.test_server + "/%s/%s/%s" % (version, orcid_id, endpoint), curl_params)
    	return read_response
    	
    def read_public(self, version, orcid_id, token, endpoint):
    	curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + token, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
    	read_response = self.orcid_curl("https://pub." + self.test_server + "/%s/%s/%s" % (version, orcid_id, endpoint), curl_params)
    	return read_response
        
        
    def test_read_limited_sections(self):
    	#Call the endpoint for each section of the limited ORCID record using 3.0
    	for item in self.sections:
    		response = self.read_members('v3.0', self.limited_orcid_id, self.limited_token, item)
    		self.assertTrue("200 OK" in response, "Read response: " + response)
    		
    def test_read_limited_items(self):
    	#Call the endpoint for each item of the limited ORCID record using 3.0
    	for item in self.limited_items:
    		response = self.read_members('v3.0', self.limited_orcid_id, self.limited_token, item)
    		self.assertTrue("200 OK" in response, "Read response: " + response)

    def test_read_limited_summaries(self):
    	#Call the endpoint for the summary of each item of the limited ORCID record using 3.0
    	for item in self.limited_summaries:
    		response = self.read_members('v3.0', self.limited_orcid_id, self.limited_token, item)
    		self.assertTrue("200 OK" in response, "Read response: " + response)
    		
    def test_read_public_sections_member_api(self):
    	#Call the endpoint for each section of the public ORCID record using 3.0 in the public API
    	for item in self.sections:
    		response = self.read_members('v3.0', self.public_orcid_id, self.memapi_public_token, item)
    		self.assertTrue("200 OK" in response, "Read response: " + response)

    def test_read_public_items_member_api(self):
    	#Call the endpoint for each item of the limited ORCID record using 3.0 in the member API
    	for item in self.public_items:
    		response = self.read_members('v3.0', self.public_orcid_id, self.memapi_public_token, item)
    		self.assertTrue("200 OK" in response, "Read response: " + response)

    def test_read_public_summaries_member_api(self):
    	#Call the endpoint for the summary of each item of the public ORCID record using 3.0 in the member API
    	for item in self.public_summaries:
    		response = self.read_members('v3.0', self.public_orcid_id, self.memapi_public_token, item)
    		self.assertTrue("200 OK" in response, "Read response: " + response)

    def test_read_public_sections_public_token(self):
    	#Call the endpoint for each section of the public ORCID record using 3.0 in the public API
    	for item in self.sections:
    		response = self.read_public('v3.0', self.public_orcid_id, self.pubapi_public_token, item)
    		self.assertTrue("200 OK" in response, "Read response: " + response)

    def test_read_public_items_public_token(self):
    	#Call the endpoint for each item of the public ORCID record using 3.0 and the public API
    	for item in self.public_items:
    		response = self.read_public('v3.0', self.public_orcid_id, self.pubapi_public_token, item)
    		self.assertTrue("200 OK" in response, "Read response: " + response)

    def test_read_public_summaries_public_token(self):
    	#Call the endpoint for the summary of each item of the public ORCID record using 3.0 and public API
    	for item in self.public_summaries:
    		response = self.read_public('v3.0', self.public_orcid_id, self.pubapi_public_token, item)
    		self.assertTrue("200 OK" in response, "Read response: " + response)

