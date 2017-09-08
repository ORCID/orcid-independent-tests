import OrcidBaseTest
import properties
import re

class PublicRecord(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        self.limited_orcid_id = '0000-0001-7325-5491'
        self.limited_token = properties.limited_token
        self.private_record_limited_token = properties.private_record_limited_token
        self.public_orcid_id    = '0000-0002-3874-7658'
        self.private_orcid_id = '0000-0003-2366-2712'
        self.private_apiadded_orcid_id = '0000-0001-6085-8875'
        self.private_apiadded_token = properties.private_apiadded_token
        self.pubapi_public_token = properties.pubapi_public_token
        self.memapi_public_token = properties.memapi_public_token
        self.saved_records_path20 = 'saved_records'
        self.saved_records_path21 = 'saved_recordsv21'
        self.saved_records_path30 = 'saved_recordsv30'
        self.version      = properties.version
        self.dates              = ['<common:created-date>','<common:last-modified-date>']
  	
    def read_record(self, access, api, orcid_id, endpoint, putcode=""):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer ' + access, '-H', 'Content-Type: application/vnd.orcid+xml', '-H', 'Accept: application/xml', '-X', 'GET']
	read_response = self.orcid_curl("https://" + api + ".qa.orcid.org/" + self.version + "/" + orcid_id + "/" + endpoint + putcode, curl_params)
	return read_response

    def compare_response(self, read_response, file):
        response_content = read_response.partition('X-Frame-Options: DENY')[2]
        response_body = re.sub('[ \t](.*)(\<common:last-modified-date\>|\<common:created-date\>)(.*)(\</common:last-modified-date\>|\</common:created-date\>)\\n','', response_content)
        if self.version == 'v2.1':
            self.assertTrue(response_body.strip() == open(self.saved_records_path21 + '/' + file,'r').read(), 'response_body: ' + response_body)
        elif self.version == 'v3.0_dev1':
            self.assertTrue(response_body.strip() == open(self.saved_records_path30 + '/' + file,'r').read(), 'response_body: ' + response_body)
        else:
            self.assertTrue(response_body.strip() == open(self.saved_records_path20 + '/' + file,'r').read(), 'response_body: ' + response_body)

    def empty_element(self, read_response):
        response_content = read_response.partition('X-Frame-Options: DENY')[2]
        self.assertTrue((re.split('\/>', response_content, 2)[1]) == '\n', 'Non empty element returned: ' + response_content)

    def private_element_9039(self, read_response):
        self.assertTrue('<error-code>9039</error-code>' in read_response, 'Expected 9039 error instead: ' + read_response)

    def private_element_9038(self, read_response):
        self.assertTrue('<error-code>9038</error-code>' in read_response, 'Expected 9038 error instead: ' + read_response)

    def private_element_9013(self, read_response):
        self.assertTrue('<error-code>9013</error-code>' in read_response, 'Expected 9013 error instead: ' + read_response)
    
#Member API, read-public token, record with limited information

    def test_limited_record_public_api_record(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'record')
        self.compare_response(read_response, 'limited_empty_record.xml')

    def test_limited_record_public_api_person(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'person')
        self.compare_response(read_response, 'limited_empty_person.xml')

    def test_limited_record_public_api_personal_details(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'personal-details')
        self.compare_response(read_response, 'limited_empty_personal_details.xml')
        
    def test_limited_record_public_api_other_names(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'educations')
        self.empty_element(read_response)
        
    def test_limited_record_member_api_other_name(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'other-names', '/2686')
        self.private_element_9038(read_response)

    def test_limited_record_member_api_bio(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'biography')
        self.private_element_9038(read_response)

    def test_limited_record_member_api_urls(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'researcher-urls')
        self.empty_element(read_response)

    def test_limited_record_member_api_url(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'researcher-urls', '/7187')
        self.private_element_9038(read_response)

    def test_limited_record_member_api_emails(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'email')
        self.empty_element(read_response)

    def test_limited_record_member_api_addresses(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'address')
        self.empty_element(read_response)

    def test_limited_record_member_api_addresses(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'address', '/1070')
        self.private_element_9038(read_response)

    def test_limited_record_member_api_keywords(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'keywords')
        self.empty_element(read_response)

    def test_limited_record_member_api_keyword(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'keywords', '/1281')
        self.private_element_9038(read_response)

    def test_limited_record_member_api_identifiers(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'external-identifiers')
        self.empty_element(read_response)

    def test_limited_record_member_api_identifier(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'external-identifiers', '/302')
        self.private_element_9038(read_response)

    def test_limited_record_member_api_activities(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'activities')
        self.compare_response(read_response, 'limited_empty_activities.xml')

    def test_limited_record_member_api_educations(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'educations')
        self.empty_element(read_response)

    def test_limited_record_member_api_education(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'education', '/1412')
        self.private_element_9038(read_response)

    def test_limited_record_member_api_employments(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'employments')
        self.empty_element(read_response)

    def test_limited_record_member_api_employment(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'employment', '/1413')
        self.private_element_9038(read_response)

    def test_limited_record_member_api_fundings(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'fundings')
        self.empty_element(read_response)

    def test_limited_record_member_api_fundings(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'funding', '/1285')
        self.private_element_9038(read_response)

    def test_limited_record_member_api_works(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'works')
        self.empty_element(read_response)

    def test_limited_record_member_api_work(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'work', '/141942')
        self.private_element_9038(read_response)

    def test_limited_record_member_api_peer_reviews(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'peer-reviews')
        self.empty_element(read_response)

    def test_limited_record_member_api_peer_review(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.limited_orcid_id, 'peer-review', '/1077')        
       

#Public API, read public token, record with public information

    def test_public_record_public_api_record(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'record')
        self.compare_response(read_response, 'public_record.xml')

    def test_public_record_public_api_person(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'person')
        self.compare_response(read_response, 'public_person.xml')

    def test_public_record_public_api_personal_details(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'personal-details')
        self.compare_response(read_response, 'public_personal_details.xml')

    def test_public_record_public_api_other_names(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'other-names')
        self.compare_response(read_response, 'public_other_names.xml')

    def test_public_record_public_api_other_name(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'other-names', '/2685')
        self.compare_response(read_response, 'public_other_name.xml')

    def test_public_record_public_api_bio(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'biography')
        self.compare_response(read_response, 'public_bio.xml')

    def test_public_record_public_api_urls(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'researcher-urls')
        self.compare_response(read_response, 'public_urls.xml')

    def test_public_record_public_api_url(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'researcher-urls', '/7186')
        self.compare_response(read_response, 'public_url.xml')

    def test_public_record_public_api_emails(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'email')
        self.compare_response(read_response, 'public_emails.xml')

    def test_public_record_public_api_addresses(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'address')
        self.compare_response(read_response, 'public_addresses.xml')

    def test_public_record_public_api_addresses(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'address', '/1069')
        self.compare_response(read_response, 'public_address.xml')

    def test_public_record_public_api_keywords(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'keywords')
        self.compare_response(read_response, 'public_keywords.xml')

    def test_public_record_public_api_keyword(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'keywords', '/1278')
        self.compare_response(read_response, 'public_keyword.xml')

    def test_public_record_public_api_identifiers(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'external-identifiers')
        self.compare_response(read_response, 'public_identifiers.xml')

    def test_public_record_public_api_identifier(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'external-identifiers', '/250')
        self.compare_response(read_response, 'public_identifier.xml')

    def test_public_record_public_api_activities(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'activities')
        self.compare_response(read_response, 'public_activities.xml')

    def test_public_record_public_api_educations(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'educations')
        self.compare_response(read_response, 'public_educations.xml')

    def test_public_record_public_api_education(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'education', '/1409')
        self.compare_response(read_response, 'public_education.xml')

    def test_public_record_public_api_employments(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'employments')
        self.compare_response(read_response, 'public_employments.xml')

    def test_public_record_public_api_employment(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'employment', '/1410')
        self.compare_response(read_response, 'public_employment.xml')

    def test_public_record_public_api_fundings(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'fundings')
        self.compare_response(read_response, 'public_fundings.xml')

    def test_public_record_public_api_fundings(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'funding', '/1284')
        self.compare_response(read_response, 'public_funding.xml')

    def test_public_record_public_api_works(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'works')
        self.compare_response(read_response, 'public_works.xml')

    def test_public_record_public_api_work(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'work', '/141941')
        self.compare_response(read_response, 'public_work.xml')

    def test_public_record_public_api_peer_reviews(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'peer-reviews')
        self.compare_response(read_response, 'public_peer_reviews.xml')

    def test_public_record_public_api_peer_review(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.public_orcid_id, 'peer-review', '/1076')
        self.compare_response(read_response, 'public_peer_review.xml')


# Member API, read-public token, record with public information

    def test_public_record_member_api_record(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'record')
        self.compare_response(read_response, 'public_record.xml')

    def test_public_record_member_api_person(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'person')
        self.compare_response(read_response, 'public_person.xml')

    def test_public_record_member_api_other_names(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'other-names')
        self.compare_response(read_response, 'public_other_names.xml')

    def test_public_record_member_api_personal_details(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'personal-details')
        self.compare_response(read_response, 'public_personal_details.xml')

    def test_public_record_member_api_other_names(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'other-names')
        self.compare_response(read_response, 'public_other_names.xml')

    def test_public_record_member_api_other_name(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'other-names', '/2685')
        self.compare_response(read_response, 'public_other_name.xml')

    def test_public_record_member_api_bio(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'biography')
        self.compare_response(read_response, 'public_bio.xml')

    def test_public_record_member_api_urls(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'researcher-urls')
        self.compare_response(read_response, 'public_urls.xml')

    def test_public_record_member_api_url(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'researcher-urls', '/7186')
        self.compare_response(read_response, 'public_url.xml')

    def test_public_record_member_api_emails(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'email')
        self.compare_response(read_response, 'public_emails.xml')

    def test_public_record_member_api_addresses(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'address')
        self.compare_response(read_response, 'public_addresses.xml')

    def test_public_record_member_api_addresses(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'address', '/1069')
        self.compare_response(read_response, 'public_address.xml')

    def test_public_record_member_api_keywords(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'keywords')
        self.compare_response(read_response, 'public_keywords.xml')

    def test_public_record_member_api_keyword(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'keywords', '/1278')
        self.compare_response(read_response, 'public_keyword.xml')

    def test_public_record_member_api_identifiers(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'external-identifiers')
        self.compare_response(read_response, 'public_identifiers.xml')

    def test_public_record_member_api_identifier(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'external-identifiers', '/250')
        self.compare_response(read_response, 'public_identifier.xml')

    def test_public_record_member_api_activities(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'activities')
        self.compare_response(read_response, 'public_activities.xml')

    def test_public_record_member_api_educations(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'educations')
        self.compare_response(read_response, 'public_educations.xml')

    def test_public_record_member_api_education(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'education', '/1409')
        self.compare_response(read_response, 'public_education.xml')

    def test_public_record_member_api_employments(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'employments')
        self.compare_response(read_response, 'public_employments.xml')

    def test_public_record_member_api_employment(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'employment', '/1410')
        self.compare_response(read_response, 'public_employment.xml')

    def test_public_record_member_api_fundings(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'fundings')
        self.compare_response(read_response, 'public_fundings.xml')

    def test_public_record_member_api_fundings(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'funding', '/1284')
        self.compare_response(read_response, 'public_funding.xml')

    def test_public_record_member_api_works(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'works')
        self.compare_response(read_response, 'public_works.xml')

    def test_public_record_member_api_work(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'work', '/141941')
        self.compare_response(read_response, 'public_work.xml')

    def test_public_record_member_api_peer_reviews(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'peer-reviews')
        self.compare_response(read_response, 'public_peer_reviews.xml')

    def test_public_record_member_api_peer_review(self):
        read_response = self.read_record(self.memapi_public_token, 'api', self.public_orcid_id, 'peer-review', '/1076')
        self.compare_response(read_response, 'public_peer_review.xml')

#Member API, read-limited token, record with limited information

    def test_limited_record_member_api_record(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'record')
        self.compare_response(read_response, 'limited_record.xml')

    def test_limited_record_member_api_person(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'person')
        self.compare_response(read_response, 'limited_person.xml')

    def test_limited_record_member_api_personal_details(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'personal-details')
        self.compare_response(read_response, 'limited_personal_details.xml')

    def test_limited_record_member_api_other_names(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'other-names')
        self.compare_response(read_response, 'limited_other_names.xml')

    def test_limited_record_member_api_other_name(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'other-names', '/2686')
        self.compare_response(read_response, 'limited_other_name.xml')

    def test_limited_record_member_api_bio(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'biography')
        self.compare_response(read_response, 'limited_bio.xml')

    def test_limited_record_member_api_urls(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'researcher-urls')
        self.compare_response(read_response, 'limited_urls.xml')

    def test_limited_record_member_api_url(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'researcher-urls', '/7187')
        self.compare_response(read_response, 'limited_url.xml')

    def test_limited_record_member_api_emails(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'email')
        self.compare_response(read_response, 'limited_emails.xml')

    def test_limited_record_member_api_addresses(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'address')
        self.compare_response(read_response, 'limited_addresses.xml')

    def test_limited_record_member_api_addresses(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'address', '/1070')
        self.compare_response(read_response, 'limited_address.xml')

    def test_limited_record_member_api_keywords(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'keywords')
        self.compare_response(read_response, 'limited_keywords.xml')

    def test_limited_record_member_api_keyword(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'keywords', '/1281')
        self.compare_response(read_response, 'limited_keyword.xml')

    def test_limited_record_member_api_identifiers(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'external-identifiers')
        self.compare_response(read_response, 'limited_identifiers.xml')

    def test_limited_record_member_api_identifier(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'external-identifiers', '/302')
        self.compare_response(read_response, 'limited_identifier.xml')

    def test_limited_record_member_api_activities(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'activities')
        self.compare_response(read_response, 'limited_activities.xml')

    def test_limited_record_member_api_educations(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'educations')
        self.compare_response(read_response, 'limited_educations.xml')

    def test_limited_record_member_api_education(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'education', '/1412')
        self.compare_response(read_response, 'limited_education.xml')

    def test_limited_record_member_api_employments(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'employments')
        self.compare_response(read_response, 'limited_employments.xml')

    def test_limited_record_member_api_employment(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'employment', '/1413')
        self.compare_response(read_response, 'limited_employment.xml')

    def test_limited_record_member_api_fundings(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'fundings')
        self.compare_response(read_response, 'limited_fundings.xml')

    def test_limited_record_member_api_fundings(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'funding', '/1285')
        self.compare_response(read_response, 'limited_funding.xml')

    def test_limited_record_member_api_works(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'works')
        self.compare_response(read_response, 'limited_works.xml')

    def test_limited_record_member_api_work(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'work', '/141942')
        self.compare_response(read_response, 'limited_work.xml')

    def test_limited_record_member_api_peer_reviews(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'peer-reviews')
        self.compare_response(read_response, 'limited_peer_reviews.xml')

    def test_limited_record_member_api_peer_review(self):
        read_response = self.read_record(self.limited_token, 'api', self.limited_orcid_id, 'peer-review', '/1077')
        self.compare_response(read_response, 'limited_peer_review.xml')   



#Public API, read-public token, record with limited information

    def test_limited_record_public_api_record(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'record')
        self.compare_response(read_response, 'limited_empty_record.xml')

    def test_limited_record_public_api_person(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'person')
        self.compare_response(read_response, 'limited_empty_person.xml')

    def test_limited_record_public_api_personal_details(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'personal-details')
        self.compare_response(read_response, 'limited_empty_personal_details.xml')
        
    def test_limited_record_public_api_other_names(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'educations')
        self.empty_element(read_response)
        
    def test_limited_record_member_api_other_name(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'other-names', '/2686')
        self.private_element_9039(read_response)

    def test_limited_record_member_api_bio(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'biography')
        self.private_element_9039(read_response)

    def test_limited_record_member_api_urls(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'researcher-urls')
        self.empty_element(read_response)

    def test_limited_record_member_api_url(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'researcher-urls', '/7187')
        self.private_element_9039(read_response)

    def test_limited_record_member_api_emails(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'email')
        self.empty_element(read_response)

    def test_limited_record_member_api_addresses(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'address')
        self.empty_element(read_response)

    def test_limited_record_member_api_addresses(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'address', '/1070')
        self.private_element_9039(read_response)

    def test_limited_record_member_api_keywords(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'keywords')
        self.empty_element(read_response)

    def test_limited_record_member_api_keyword(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'keywords', '/1281')
        self.private_element_9039(read_response)

    def test_limited_record_member_api_identifiers(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'external-identifiers')
        self.empty_element(read_response)

    def test_limited_record_member_api_identifier(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'external-identifiers', '/302')
        self.private_element_9039(read_response)

    def test_limited_record_member_api_activities(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'activities')
        self.compare_response(read_response, 'limited_empty_activities.xml')

    def test_limited_record_member_api_educations(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'educations')
        self.empty_element(read_response)

    def test_limited_record_member_api_education(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'education', '/1412')
        self.private_element_9039(read_response)

    def test_limited_record_member_api_employments(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'employments')
        self.empty_element(read_response)

    def test_limited_record_member_api_employment(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'employment', '/1413')
        self.private_element_9039(read_response)

    def test_limited_record_member_api_fundings(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'fundings')
        self.empty_element(read_response)

    def test_limited_record_member_api_fundings(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'funding', '/1285')
        self.private_element_9039(read_response)

    def test_limited_record_member_api_works(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'works')
        self.empty_element(read_response)

    def test_limited_record_member_api_work(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'work', '/141942')
        self.private_element_9039(read_response)

    def test_limited_record_member_api_peer_reviews(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'peer-reviews')
        self.empty_element(read_response)

    def test_limited_record_member_api_peer_review(self):
        read_response = self.read_record(self.pubapi_public_token, 'pub', self.limited_orcid_id, 'peer-review', '/1077')
        
#Member API, read-limited token, record with private information

    def test_private_record_limited_token_record(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'record')
        self.compare_response(read_response, 'private_empty_record.xml')

    def test_private_record_limited_token_person(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'person')
        self.compare_response(read_response, 'private_empty_person.xml')

    def test_private_record_limited_token_personal_details(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'personal-details')
        self.compare_response(read_response, 'private_empty_personal_details.xml')
        
    def test_private_record_limited_token_other_names(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'educations')
        self.empty_element(read_response)
        
    def test_limited_record_member_api_other_name(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'other-names', '/2687')
        self.private_element_9013(read_response)

    def test_limited_record_member_api_bio(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'biography')
        self.private_element_9013(read_response)

    def test_limited_record_member_api_urls(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'researcher-urls')
        self.empty_element(read_response)

    def test_limited_record_member_api_url(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'researcher-urls', '/7188')
        self.private_element_9013(read_response)

    def test_limited_record_member_api_emails(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'email')
        self.empty_element(read_response)

    def test_limited_record_member_api_addresses(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'address')
        self.empty_element(read_response)

    def test_limited_record_member_api_addresses(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'address', '/1071')
        self.private_element_9013(read_response)

    def test_limited_record_member_api_keywords(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'keywords')
        self.empty_element(read_response)

    def test_limited_record_member_api_keyword(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'keywords', '/1283')
        self.private_element_9013(read_response)

    def test_limited_record_member_api_identifiers(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'external-identifiers')
        self.empty_element(read_response)

    def test_limited_record_member_api_identifier(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'external-identifiers', '/576')
        self.private_element_9013(read_response)

    def test_limited_record_member_api_activities(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'activities')
        self.compare_response(read_response, 'private_empty_activities.xml')

    def test_limited_record_member_api_educations(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'educations')
        self.empty_element(read_response)

    def test_limited_record_member_api_education(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'education', '/1414')
        self.private_element_9013(read_response)

    def test_limited_record_member_api_employments(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'employments')
        self.empty_element(read_response)

    def test_limited_record_member_api_employment(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'employment', '/1415')
        self.private_element_9013(read_response)

    def test_limited_record_member_api_fundings(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'fundings')
        self.empty_element(read_response)

    def test_limited_record_member_api_fundings(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'funding', '/1286')
        self.private_element_9013(read_response)

    def test_limited_record_member_api_works(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'works')
        self.empty_element(read_response)

    def test_limited_record_member_api_work(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'work', '/141943')
        self.private_element_9013(read_response)

    def test_limited_record_member_api_peer_reviews(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'peer-reviews')
        self.empty_element(read_response)

    def test_limited_record_member_api_peer_review(self):
        read_response = self.read_record(self.private_record_limited_token, 'api', self.private_orcid_id, 'peer-review', '/1078')

