import subprocess
import json
import OrcidBaseTest

# Choose which records gets cleared, 
# 1 for step 1 tests ("Independent Test Record") 
# 2 for step 2 tests ("Testing Searchvalue")
# USER OBO
#    member_name = "OBO User Testing Client"
#    orcid_id = "0000-0002-7361-1027"
#    access_token = "7da424d0-ea30-46f9-9154-c9a80139ec63"
#        self.member_name = "Testing Andrej"
#        self.access_token = "912f0fcf-f96c-41e4-86ed-c016d96168a4"

class DeleteContent():
    def __init__(self):
        self.step = 2
        self.member_name = "Automated Test Helper"
        self.orcid_id = "0000-0001-6009-1985"
        self.access_token = "e4ed35be-6c4f-4ffc-9997-8572cc865663"
        self.webhook_token = "af36161d-0971-4ac6-b860-5bb3f7cdef64"
    #    self.member_name = "Testing Andrej"
    #    self.access_token = "912f0fcf-f96c-41e4-86ed-c016d96168a4"
        if self.step == 1:
            self.member_name = "Manual Testing Client"
            self.orcid_id = "0000-0002-7361-1027"
            self.access_token = "06702255-c514-4ecc-a225-9c48446a9173"

    def main(self):
        # Load the summary of the relevant record
        record = json.loads(self.get_record(self.access_token))

        # Remove biography items
        self.delete_bio(record['person'], "other-names", "other-name", self.member_name, self.access_token)
        self.delete_bio(record['person'], "addresses", "address", self.member_name, self.access_token)
        self.delete_bio(record['person'], "keywords", "keyword", self.member_name, self.access_token)
        self.delete_bio(record['person'], "external-identifiers", "external-identifier", self.member_name, self.access_token)
        self.delete_bio(record['person'], "researcher-urls", "researcher-url", self.member_name, self.access_token)

        # Remove work items
        self.delete_work(record['activities-summary'], self.member_name, self.access_token)

        # Remove webhook
        if self.step == 2:
            curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % self.webhook_token, '-H', 'Content-Length: 0', '-H','Accept: application/json', '-k', '-X', 'DELETE']
            self.orcid_curl("https://api.qa.orcid.org/" + self.orcid_id + "/webhook/http%3A%2F%2Fnowhere3.com%2Fupdated", curl_params)

    def obo_user(self):
        self.member_name = "OBO User Testing Client"
        self.orcid_id = "0000-0001-6009-1985"
        self.access_token = "bcbdc7bc-43ec-4f04-980d-085b45a16135"
        record = json.loads(self.get_record(self.access_token))
        self.delete_work(record['activities-summary'], self.member_name, self.access_token)

    def obo_member(self):
        self.member_name = "Member OBO Testing Client"
        self.orcid_id = "0000-0001-6009-1985"
        self.access_token = "4f762d41-5053-4df2-967e-dfd57f4cc9a5"
        record = json.loads(self.get_record(self.access_token))
        self.delete_work(record['activities-summary'], self.member_name, self.access_token)

    def orcid_curl(self, url, curl_opts):
        curl_call = ["curl"] + curl_opts + [url]
        try:
            p = subprocess.Popen(curl_call, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(subprocess.list2cmdline(curl_call))
            output, err = p.communicate()
            return output
        except Exception as e:
            raise Exception(e)

    def get_record(self, token):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % token, '-H', 'Content-Length: 0', '-H',
                       'Accept: application/json', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s" % (self.orcid_id, "record"), curl_params)
        return response.partition('X-Frame-Options: DENY')[2]

    def delete_bio(self, record, endpoint, endpoint_value, source_name, token):
        for x in record[endpoint][endpoint_value]:
            print source_name
            if x['source']['source-name']['value'] == source_name:
                if endpoint == "external-identifiers" or endpoint == "researcher-urls" or endpoint == "keywords" or endpoint == "other-names":
                    self.delete(x['put-code'], endpoint, token)
                else:
                    self.delete(x['put-code'], endpoint_value, token)

    def delete_work(self, record, source_name, token):
        for x in record['educations']['affiliation-group']:
            for y in x['summaries']:
                if y['education-summary']['source']['source-name']['value'] == source_name:
                    self.delete(y['education-summary']['put-code'], "education", token)

        for x in record['employments']['affiliation-group']:
            for y in x['summaries']:
                if y['employment-summary']['source']['source-name']['value'] == source_name:
                    self.delete(y['employment-summary']['put-code'], "employment", token)

        for x in record['distinctions']['affiliation-group']:
            for y in x['summaries']:
                if y['distinction-summary']['source']['source-name']['value'] == source_name:
                    self.delete(y['distinction-summary']['put-code'], "distinction", token)

        for x in record['services']['affiliation-group']:
            for y in x['summaries']:
                if y['service-summary']['source']['source-name']['value'] == source_name:
                    self.delete(y['service-summary']['put-code'], "service", token)

        for x in record['fundings']['group']:
            for y in x['funding-summary']:
                if y['source']['source-name']['value'] == source_name:
                    self.delete(y['put-code'], "funding", token)

        for x in record['research-resources']['group']:
            for y in x['research-resource-summary']:
                if y['source']['source-name']['value'] == source_name:
                    self.delete(y['put-code'], "research-resource", token)

        for x in record['invited-positions']['affiliation-group']:
            for y in x['summaries']:
                if y['invited-position-summary']['source']['source-name']['value'] == source_name:
                   self.delete(y['invited-position-summary']['put-code'], "invited-position", token)

        for x in record['works']['group']:
            for y in x['work-summary']:
                print(y['source']['source-name']['value'])
                print(source_name)
                print(y['source'])
                if y['source']['source-name']['value'] == source_name:
                    self.delete(y['put-code'], "work", token)
                if y['source']['assertion-origin-name']['value']:
                  if y['source']['assertion-origin-name']['value'] == source_name:
                      self.delete(y['put-code'], "work", token)

        for x in record['memberships']['affiliation-group']:
            for y in x['summaries']:
                if y['membership-summary']['source']['source-name']['value'] == source_name:
                    self.delete(y['membership-summary']['put-code'], "membership", token)

        for x in record['qualifications']['affiliation-group']:
            for y in x['summaries']:
                if y['qualification-summary']['source']['source-name']['value'] == source_name:
                    self.delete(y['qualification-summary']['put-code'], "qualification", token)

        for x in record['peer-reviews']['group']:
            for y in x['peer-review-group']:
                if y['peer-review-summary'][0]['source']['source-name']['value'] == source_name:
                    self.delete(y['peer-review-summary'][0]['put-code'], "peer-review", token)

    def delete(self, putcode, endpoint, token):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % token, '-H', 'Content-Length: 0', '-H',
                       'Accept: application/json', '-k', '-X', 'DELETE']
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), curl_params)
        print(response)
        print ("****************** %s deleted ******************" % endpoint)
        print ("")


DeleteContent().main()
DeleteContent().obo_user()
#DeleteContent().obo_member()