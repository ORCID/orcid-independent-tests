import OrcidBaseTest
import pyjavaproperties
import json

class Member12ApiReadDelete(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test.properties'))
        self.orcid_props   = p
        self.orcid_id            = self.orcid_props['orcidId']
        self.client_id           = self.orcid_props['memberClientId']
        self.client_secret       = self.orcid_props['memberClientSecret']        
        self.code                = self.orcid_props['api2PostUpdateCode']
        self.token, self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)

    def test_get12_orcidworks(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("http://pub.qa.orcid.org/v1.2/%s/orcid-works" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        orcid_works = json_response.get("orcid-profile").get("orcid-activities").get("orcid-works")
        if (len(orcid_works) > 0):
            for w in orcid_works["orcid-work"]:
                delete_results = self.remove_by_putcode(w["put-code"])
                self.assertEquals("", str(delete_results))
        
    ''' TODO curls executes with different orcid-id
    def test_get20_works(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://pub.qa.orcid.org/v2.0/%s/works" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        group = json_response.get("group")
        self.assertIsNotNone(group, "Group not found in JSON")
        if (len(group) > 0):
            for s in group:
                putcode = s["summary"][0]["put-code"]
                delete_results = self.remove_by_putcode(putcode, 'work')
                self.assertEquals("", str(delete_results))'''

    def test_get20_fundings(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://pub.qa.orcid.org/v2.0/%s/fundings" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        group = json_response.get("group")
        self.assertIsNotNone(group, "Group not found in JSON")
        if (len(group) > 0):
            for s in group:
                putcode = s["funding-summary"][0]["put-code"]
                delete_results = self.remove_by_putcode(putcode, 'funding')
                self.assertEquals("", str(delete_results))

    ''' TODO educations does not contain {group} in JSON response
    def test_get20_educations(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://pub.qa.orcid.org/v2.0/%s/educations" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        group = json_response.get("group")
        self.assertIsNotNone(group, "Group not found in JSON")
        if (len(group) > 0):
            for s in group:
                putcode = s["education-summary"][0]["put-code"]
                delete_results = self.remove_by_putcode(putcode, 'education')
                self.assertEquals("", str(delete_results))'''

    def test_get20_educations2(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://pub.qa.orcid.org/v2.0/%s/educations" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        es = json_response.get("education-summary")
        self.assertIsNotNone(es, "education-summary not found in JSON")
        if (len(es) > 0):
            for e in es:
                putcode = e["put-code"]
                delete_results = self.remove_by_putcode(putcode, 'education')
                self.assertEquals("", str(delete_results))
                
    ''' TODO work in progress
    def test_get_activities(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://pub.qa.orcid.org/v2.0/%s/activities" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        orcid_works = json_response.get("works").get("group")
        #self.assertTrue(False, "activities: " + str(orcid_works))
        codes = ""
        if (len(orcid_works) > 0):
            for ws in orcid_works["work-summary"]:
                for w in ws:
                    codes = str(w["put-code"]) + " - " + codes
        self.assertTrue(False, "JSON: " + codes + " Found: " + str(len(orcid_works)))'''
        
        
        