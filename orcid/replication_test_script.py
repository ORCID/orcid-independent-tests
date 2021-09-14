import subprocess
import time
import json
import unittest
import random
import threading
import xml.dom.minidom as md

class Replication(unittest.TestCase):
    def __init__(self):
        self.orcid_id = "0000-0001-6009-1985"
        self.access_token = "715ee62c-573e-4cdd-beff-6baae3890cce"     
        self.source = "Automated Test Helper"
        self.curl_params_get = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % self.access_token, '-H', 'Content-Length: 0', '-H', 'Accept: application/json', '-k', '-X', 'GET']
        '''if properties.type == "actions":
          self.test_server = properties.test_server
          self.access_token = properties.staticAccess
        else:
          self.test_server = local_properties.test_server
          self.access_token = properties.staticAccess'''
    def get_record(self, token):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % token, '-H', 'Content-Length: 0', '-H', 'Accept: application/json', '-k', '-X', 'GET']
        
            
    def cleanup(self):
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/record" % self.orcid_id, self.curl_params_get)
        print ("{" + response.partition('{')[2])
        record = json.loads("{" + response.partition('{')[2])['activities-summary']
        try:
            for x in record['educations']['affiliation-group']:
                for y in x['summaries']:
                    if y['education-summary']['source']['source-name']['value'] == self.source:
                        self.delete_activity(y['education-summary']['put-code'], "education")
                        print("edu deleted")

            for x in record['fundings']['group']:
                for y in x['funding-summary']:
                    if y['source']['source-name']['value'] == self.source:
                        self.delete_activity(y['put-code'], "funding")
                        print("funding deleted")

            for x in record['works']['group']:
                for y in x['work-summary']:
                    if y['source']['source-name']['value'] == self.source:
                        self.delete_activity(y['put-code'], "work")
                        if y['source']['assertion-origin-name']['value']:
                          if y['source']['assertion-origin-name']['value'] == self.source:
                            self.delete_activity(y['put-code'], "work")
                            print("work deleted")

            for x in record['peer-reviews']['group']:
                for y in x['peer-review-group']:
                    if y['peer-review-summary'][0]['source']['source-name']['value'] == self.source:
                        self.delete_activity(y['peer-review-summary'][0]['put-code'], "peer-review")
                        print("pr deleted")
        except TypeError as e:
            raise (e)                        
    
    def orcid_curl(self, url, curl_opts, rec=False):
        curl_call = ["curl"] + curl_opts + [url]
        while True:
            try:
                p = subprocess.Popen(curl_call, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                #print(subprocess.list2cmdline(curl_call))
                output,err = p.communicate()
                return output.decode()
            except Exception as e:
                raise Exception(e)
            break
            
    def getputcode(self, post_response):
        putcode = ''
        for header in post_response.split('\n'):
            if("Location:" in header):
                location_chunks = header.split('/')
                putcode = location_chunks[-1].strip()
        return putcode
            
            
    def update_xml(self, xml_file, tag, value, put=False):
        file = md.parse( "../post_files/" + xml_file) 
        file.getElementsByTagName(tag)[0].firstChild.nodeValue = value
        root = file.documentElement
        if put:
            root.setAttribute("put-code", value)
        else:
            if (root.hasAttribute("put-code")):
                root.removeAttribute("put-code")
        with open("../post_files/" + xml_file, "w") as fs: 
            fs.write(file.toxml())
            fs.close()     
        
    def update_activity(self, endpoint, putcode, xml_file):
        self.update_xml(xml_file, "common:external-id-value", putcode, True)
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + self.access_token, '-H',
                       'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + "../post_files/" + xml_file, '-X', 'PUT']
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), curl_params)
    
    def post_activity(self, endpoint, xml_file, count):
        self.update_xml(xml_file, "common:external-id-value", count)
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + self.access_token, '-H',
                       'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', '@' + "../post_files/" + xml_file, '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s" % (self.orcid_id, endpoint), curl_params)
        putcode = self.getputcode(response)        
        return putcode
    
    def delete_activity(self, endpoint, putcode):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % self.access_token, '-H', 'Content-Length: 0', '-H', 'Accept: application/orcid+xml', '-k', '-X', 'DELETE']
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), curl_params)

    def confirmAddedWorks(self, endpoint, putcode):
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), self.curl_params_get)
        self.assertTrue("HTTP/1.1 200" in response, "200 code missing from response: \n" + response)
        
    def confirmUpdatedWorks(self, endpoint, putcode):
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), self.curl_params_get)
        self.assertTrue('"external-id-value":"%s"' % putcode in response, "Putcode %s missing from external identifier in response: \n" % putcode + response)
        
    def confirmRemovedWorks(self, endpoint, putcode):
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), self.curl_params_get)
        self.assertTrue("HTTP/1.1 404" in response, "404 code missing from response: \n" + response)
    
    def replicationTest(self, thread_name, endpoint, xml_file):
        count = 0
        putcodes = []
        updatedPutcodes = []
        deletedPutcodes = []
        while count < 10:
            putcode = self.post_activity(endpoint, xml_file, count)
            putcodes.append(putcode)       
            print("%s: %s %s added" % (thread_name, endpoint, putcode))
            count += 1
            
        print (thread_name, ": ", putcodes)
        for putcode in putcodes:
            self.confirmAddedWorks(endpoint, putcode)
        print("%s: Confirmation - %ss added" % (thread_name, endpoint))
        
        updatedPutcodes = random.sample(putcodes, 5)
        for putcode in updatedPutcodes:
            self.update_activity(endpoint, putcode, xml_file)
            print("%s: %s %s updated" % (thread_name, endpoint, putcode))
        for putcode in updatedPutcodes:
            self.confirmUpdatedWorks(endpoint, putcode)
        print("%s: Confirmation - %ss updated" % (thread_name, endpoint))
        
        deletedPutcodes = random.sample(putcodes, 5)
        for putcode in deletedPutcodes:
            self.delete_activity(endpoint, putcode)
            print("%s: %s %s deleted" % (thread_name, endpoint, putcode))
        for putcode in deletedPutcodes:
            self.confirmRemovedWorks(endpoint, putcode)
        print("%s: Confirmation - %ss removed" % (thread_name, endpoint))
        
    def main(self):
        t1 = threading.Thread(target=self.replicationTest, args=("Thread-1", "work", "test_work.xml") )
        t2 = threading.Thread(target=self.replicationTest, args=("Thread-2", "education", "test_edu.xml") )
        t3 = threading.Thread(target=self.replicationTest, args=("Thread-3", "funding", "test_funding.xml") )
        t4 = threading.Thread(target=self.replicationTest, args=("Thread-4", "peer-review", "test_pr.xml") )
        print("Cleaning record...")
        self.cleanup()
        print("Cleaning done")
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        

Replication().main()
