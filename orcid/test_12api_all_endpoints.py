import OrcidBaseTest
import pyjavaproperties

class Api12PostUpdateDelete(OrcidBaseTest.OrcidBaseTest):
    
    xml_data_files_path = 'post_files/'

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test.properties'))
        self.orcid_props   = p
        self.orcid_id    = self.orcid_props['staticId']
        self.access      = self.orcid_props['staticAccess']

#Works section 1.2
    def test_01post_work_12(self):
        #post a work with 1.2
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '12postwork.xml', '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/orcid-works" % self.orcid_id, curl_params)
        self.assertTrue("201 Created" in response, "response: " + response)

    def test_02put_work_12(self):
        #update the work with 1.2
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '12putwork.xml', '-X', 'PUT']
        response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/orcid-works" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)
        
    def test_03read_work_12(self):
        #read the record to check 1. the posted work was updated and 2. the manually added work was not affected
	curl_params = ['-L', '-i', '-k', '-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.access, '-X', 'GET']
	response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/orcid-works" % self.orcid_id, curl_params)
	self.assertTrue("<work-external-identifier-id>9999</work-external-identifier-id>" in response and "<work-external-identifier-id>1234</work-external-identifier-id>" not in response, "response: " + response)

    def test_04delete_work_12(self):
        #delete the works by putting an empty work
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '12emptywork.xml', '-X', 'PUT']
        response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/orcid-works" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)

#Affiliations section 1.2
    def test_05post_affiliation_12(self):
        #post an affiliation with 1.2
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '12postaffiliation.xml', '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/affiliations" % self.orcid_id, curl_params)
        self.assertTrue("201 Created" in response, "response: " + response)

    def test_06put_affiliation_12(self):
        #update the affiliation with 1.2
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '12putaffiliation.xml', '-X', 'PUT']
        response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/affiliations" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)
        
    def test_07read_affiliation_12(self):
        #read the record to check 1. the posted affiliation was updated and 2. the manually added affiliation was not affected
	curl_params = ['-L', '-i', '-k', '-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.access, '-X', 'GET']
	response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/affiliations" % self.orcid_id, curl_params)
	self.assertTrue("<disambiguated-organization-identifier>2167</disambiguated-organization-identifier>" in response and "<department-name>1.2 Put</department-name>" in response, "response: " + response)

    def test_08delete_affiliation_12(self):
        #delete the affiliations by putting an empty affiliation
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '12emptyaffiliation.xml', '-X', 'PUT']
        response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/affiliations" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)

#Funding section 1.2
    def test_09post_funding_12(self):
        #post a funding item with 1.2
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '12postfunding.xml', '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/funding" % self.orcid_id, curl_params)
        self.assertTrue("201 Created" in response, "response: " + response)

    def test_10put_funding_12(self):
        #update the funding item with 1.2
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '12putfunding.xml', '-X', 'PUT']
        response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/funding" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)
        
    def test_11read_funding_12(self):
        #read the record to check 1. the posted funding item was updated and 2. the manually added funding item was not affected
	curl_params = ['-L', '-i', '-k', '-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.access, '-X', 'GET']
	response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/funding" % self.orcid_id, curl_params)
	self.assertTrue("<funding-external-identifier-value>8888</funding-external-identifier-value>" in response and "<funding-external-identifier-value>1234</funding-external-identifier-value>" not in response, "response: " + response)

    def test_12delete_funding_12(self):
        #delete the funding item by putting an funding section
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '12emptyfunding.xml', '-X', 'PUT']
        response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/funding" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)

#Biography section 1.2
    def test_13post_externalid_12(self):
        #post an external identifier with 1.2
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '12postidentifier.xml', '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/orcid-bio/external-identifiers" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)

    def test_14put_bio_12(self):
        #update external identifier and add a keyword item with 1.2
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '12putbio.xml', '-X', 'PUT']
        response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/orcid-bio" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)
        
    def test_15read_bio_12(self):
        #read the record to check 1. the external identifier was updated and 2. the manually added sections were not affected
	curl_params = ['-L', '-i', '-k', '-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.access, '-X', 'GET']
	response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/orcid-bio" % self.orcid_id, curl_params)
	self.assertTrue("<external-id-reference>5555</external-id-reference>" in response and "<keyword>bananas</keyword>" in response, "response: " + response)

    def test_16delete_bio_12(self):
        #delete the keyword and external identifier by putting empty sections
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '12emptybio.xml', '-X', 'PUT']
        response = self.orcid_curl("https://api.qa.orcid.org/v1.2/%s/orcid-bio" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)
        
#read the record: curl -H 'Content-Type: application/orcid+xml' -H 'Authorization: Bearer f4f35385-f903-451c-9a15-cde960dca66b' -X GET 'http://api.qa.orcid.org/v1.2/0000-0002-7361-1027/orcid-profile' -L -i -k
