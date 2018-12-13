# Write bulk works test. This is a stand alone test. I think we could include in the allendpoints test eventually.
# This is just to show working.
# I also think we could/ should test for whether there are any errors maybe in the post?
# Since our error handling will post still if there is an error in the XML.



# Imports
import OrcidBaseTest
import properties


#define Class
class BulkWorks(OrcidBaseTest.OrcidBaseTest):
    #Definitions
    # def setUp(self):
    #     self.client_id = properties.bulk_works_client
    #     self.client_secret = properties.bulk_works_secret
    #     self.notify_token = properties.notifyToken
    #     self.orcid_id = properties.bulk_works_orcidId
    #     self.access = properties.bulk_works_token

    xml_data_files_path = 'post_files/'
#Set up properties
    def setUp(self):
        self.client_id = properties.memberClientId
        self.client_secret = properties.memberClientSecret
        self.notify_token = properties.notifyToken
        self.orcid_id = properties.staticId
        self.access = properties.staticAccess

        
    def test_bulkwork_3(self):
        #Test posting a bulk work returns a 200 OK response
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + self.xml_data_files_path + '30rc1postbulkworks.xml', '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0_rc1/%s/works" % self.orcid_id, curl_params)
        self.assertTrue("200 OK" in response, "response: " + response)
