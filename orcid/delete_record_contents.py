import subprocess
import json

# Choose which records gets cleared, 
# 1 for step 1 tests ("Independent Test Record") 
# 2 for step 2 tests ("Testing Searchvalue")
# USER OBO
#    member_name = "OBO User Testing Client"
#    orcid_id = "0000-0002-7361-1027"
#    access_token = "7da424d0-ea30-46f9-9154-c9a80139ec63"
step = 1
if step == 1:
    member_name = "Manual Testing Client"
    orcid_id = "0000-0002-7361-1027"
    access_token = "06702255-c514-4ecc-a225-9c48446a9173"
else:
    member_name = "Testing Andrej"
    orcid_id = "0000-0001-6009-1985"
    access_token = "299e0132-623d-4024-9b47-6c9a0e042b39"
    webhook_token = "af36161d-0971-4ac6-b860-5bb3f7cdef64"

putcodes = []

def main():
    # Load the summary of the relevant record
    record = json.loads(get_record())

    # Remove biography items
    delete_bio(record['person'], "other-names", "other-name", member_name)
    delete_bio(record['person'], "addresses", "address", member_name)
    delete_bio(record['person'], "keywords", "keyword", member_name)
    delete_bio(record['person'], "external-identifiers", "external-identifier", member_name)
    delete_bio(record['person'], "researcher-urls", "researcher-url", member_name)

    # Remove work items
    delete_work(record['activities-summary'], member_name)

    # Remove webhook
    if step == 2:
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % webhook_token, '-H', 'Content-Length: 0', '-H','Accept: application/json', '-k', '-X', 'DELETE']
        orcid_curl("https://api.qa.orcid.org/" + orcid_id + "/webhook/http%3A%2F%2Fnowhere3.com%2Fupdated", curl_params)

def orcid_curl(url, curl_opts):
    curl_call = ["curl"] + curl_opts + [url]
    try:
        p = subprocess.Popen(curl_call, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(subprocess.list2cmdline(curl_call))
        output, err = p.communicate()
        return output
    except Exception as e:
        raise Exception(e)

def get_record():
    curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % access_token, '-H', 'Content-Length: 0', '-H',
                   'Accept: application/json', '-k', '-X', 'GET']
    response = orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s" % (orcid_id, "record"), curl_params)
    return response.partition('X-Frame-Options: DENY')[2]


def delete_bio(record, endpoint, endpoint_value, source_name):
    for x in record[endpoint][endpoint_value]:
        if x['source']['source-name']['value'] == source_name:
            if endpoint == "external-identifiers" or endpoint == "researcher-urls" or endpoint == "keywords" or endpoint == "other-names":
                delete(x['put-code'], endpoint)
            else:
                delete(x['put-code'], endpoint_value)


def delete_work(record, source_name):
    for x in record['educations']['affiliation-group']:
        for y in x['summaries']:
            if y['education-summary']['source']['source-name']['value'] == source_name:
                delete(y['education-summary']['put-code'], "education")

    for x in record['employments']['affiliation-group']:
        for y in x['summaries']:
            if y['employment-summary']['source']['source-name']['value'] == source_name:
                delete(y['employment-summary']['put-code'], "employment")

    for x in record['distinctions']['affiliation-group']:
        for y in x['summaries']:
            if y['distinction-summary']['source']['source-name']['value'] == source_name:
                delete(y['distinction-summary']['put-code'], "distinction")

    for x in record['services']['affiliation-group']:
        for y in x['summaries']:
            if y['service-summary']['source']['source-name']['value'] == source_name:
                delete(y['service-summary']['put-code'], "service")

    for x in record['fundings']['group']:
        for y in x['funding-summary']:
            if y['source']['source-name']['value'] == source_name:
                delete(y['put-code'], "funding")

    for x in record['research-resources']['group']:
        for y in x['research-resource-summary']:
            if y['source']['source-name']['value'] == source_name:
                delete(y['put-code'], "research-resource")

    for x in record['invited-positions']['affiliation-group']:
        for y in x['summaries']:
            if y['invited-position-summary']['source']['source-name']['value'] == source_name:
               delete(y['invited-position-summary']['put-code'], "invited-position")

    for x in record['works']['group']:
        for y in x['work-summary']:
            if y['source']['source-name']['value'] == source_name:
                delete(y['put-code'], "work")

    for x in record['memberships']['affiliation-group']:
        for y in x['summaries']:
            if y['membership-summary']['source']['source-name']['value'] == source_name:
                delete(y['membership-summary']['put-code'], "membership")

    for x in record['qualifications']['affiliation-group']:
        for y in x['summaries']:
            if y['qualification-summary']['source']['source-name']['value'] == source_name:
                delete(y['qualification-summary']['put-code'], "qualification")

    for x in record['peer-reviews']['group']:
        for y in x['peer-review-group']:
            if y['peer-review-summary'][0]['source']['source-name']['value'] == source_name:
                delete(y['peer-review-summary'][0]['put-code'], "peer-review")


def delete(putcode, endpoint):

    curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % access_token, '-H', 'Content-Length: 0', '-H',
                   'Accept: application/json', '-k', '-X', 'DELETE']
    response = orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s/%s" % (orcid_id, endpoint, putcode), curl_params)
    print(response)
    print ("****************** %s deleted ******************" % endpoint)
    print ("")

main()
