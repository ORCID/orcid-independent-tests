import OrcidBaseTest
import json
import properties
import local_properties

class ApiReadDelete(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        if local_properties.type == "jenkins":
          self.test_server = properties.test_server
        else:
          self.test_server = local_properties.test_server
        self.scope               = "/read-limited%20/activities/update%20/person/update"
        self.orcid_id            = properties.orcidId
        self.client_id           = properties.memberClientId
        self.client_secret       = properties.memberClientSecret
        self.webhook_access      = self.orcid_generate_token(self.client_id, self.client_secret, "/webhook")
        self.code                = self.generate_auth_code(self.client_id, self.scope, "api2PostUpdateCode")
        self.token, self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
        self.version             ="/v2.0/"

    def test_get20_works(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://api." + properties.test_server + "/v2.0/%s/works" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        group = json_response.get("group")
        self.assertIsNotNone(group, "Group not found in JSON")
        if (len(group) > 0):
            for s in group:
                putcode = s["work-summary"][0]["put-code"]
                delete_results = self.remove_by_putcode(self.version, putcode, 'work')
                #self.assertEquals("", str(delete_results))

    def test_get20_fundings(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/%s/fundings" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        group = json_response.get("group")
        self.assertIsNotNone(group, "Group not found in JSON")
        if (len(group) > 0):
            for s in group:
                putcode = s["funding-summary"][0]["put-code"]
                delete_results = self.remove_by_putcode(self.version, putcode, 'funding')
                #self.assertEquals("", str(delete_results))

    def test_get20_reviews(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/%s/peer-reviews" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        group = json_response.get("group")
        self.assertIsNotNone(group, "Group not found in JSON")
        if (len(group) > 0):
            for s in group:
                putcode = s["peer-review-summary"][0]["put-code"]
                delete_results = self.remove_by_putcode(self.version, putcode, 'peer-review')
                #self.assertEquals("", str(delete_results))

    def test_get20_educations(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/%s/educations" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        es = json_response.get("education-summary")
        self.assertIsNotNone(es, "education-summary not found in JSON")
        if (len(es) > 0):
            for e in es:
                putcode = e["put-code"]
                delete_results = self.remove_by_putcode(self.version, putcode, 'education')
                #self.assertEquals("", str(delete_results))

    def test_remove_keywords(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/%s/keywords" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        es = json_response.get("keyword")
        self.assertIsNotNone(es, "keyword not found in JSON")
        if (len(es) > 0):
            for e in es:
                putcode = e["put-code"]
                delete_results = self.remove_by_putcode(self.version, putcode, 'keyword')

    def test_remove_externalids(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/%s/external-identifiers" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        es = json_response.get("external-identifier")
        self.assertIsNotNone(es, "external-identifier not found in JSON")
        if (len(es) > 0):
            for e in es:
                putcode = e["put-code"]
                delete_results = self.remove_by_putcode(self.version, putcode, 'external-identifier')

    def test_remove_country(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/%s/address" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        es = json_response.get("address")
        self.assertIsNotNone(es, "address not found in JSON")
        if (len(es) > 0):
            for e in es:
                putcode = e["put-code"]
                delete_results = self.remove_by_putcode(self.version, putcode, 'address')

    def test_remove_other_names(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/%s/other-names" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        es = json_response.get("other-name")
        self.assertIsNotNone(es, "other-name not found in JSON")
        if (len(es) > 0):
            for e in es:
                putcode = e["put-code"]
                delete_results = self.remove_by_putcode(self.version, putcode, 'other-names')

    def test_remove_websites(self):
        self.assertIsNotNone(self.token, "No token generated")
        curl_params = ['-H', 'Content-Type: application/orcid+json', '-H', 'Accept: application/json', '-H', 'Authorization: Bearer ' + str(self.token)]
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/%s/researcher-urls" % self.orcid_id, curl_params)
        json_response = json.loads(response)
        es = json_response.get("researcher-url")
        self.assertIsNotNone(es, "researcher-url not found in JSON")
        if (len(es) > 0):
            for e in es:
                putcode = e["put-code"]
                delete_results = self.remove_by_putcode(self.version, putcode, 'researcher-urls')

    def test_remove_webhook(self):
        self.assertIsNotNone(self.webhook_access, "No token generated")
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + self.webhook_access, '-H', 'Content-Length: 0', '-H', 'Accept: application/json', '-k', '-X', 'DELETE']
        response = self.orcid_curl("http://api." + self.test_server + "/%s/webhook/%s" % (self.orcid_id, "http%3A%2F%2Fnowhere3.com%2Fupdated"), curl_params)

