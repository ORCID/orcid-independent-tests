import subprocess
import re
import os
import time
import json
import unittest
import random
import threading
import logging
import xml.dom.minidom as md

class Replication(unittest.TestCase):
    def __init__(self):
        self.orcid_id = "0000-0001-6009-1985"
        self.access_token = "715ee62c-573e-4cdd-beff-6baae3890cce"     
        self.source = "Automated Test Helper"
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.curl_params_get = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % self.access_token, '-H', 'Content-Length: 0', '-H', 'Accept: application/json', '-k', '-X', 'GET']
        '''if properties.type == "actions":
          self.test_server = properties.test_server
          self.access_token = properties.staticAccess
        else:
          self.test_server = local_properties.test_server
          self.access_token = properties.staticAccess'''
            
    def cleanup(self):
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/record" % self.orcid_id, self.curl_params_get, None)
        record = json.loads("{" + response.partition('{')[2])['activities-summary']
        try:
            print("Education: ", end="", flush=True)
            if record['educations']['affiliation-group']:
                for x in record['educations']['affiliation-group']:
                    for y in x['summaries']:                    
                        if y['education-summary']['source']['source-name']['value'] == self.source:
                            self.delete_activity("education", y['education-summary']['put-code'], None)                        
                            print(y['education-summary']['put-code'], "", end="", flush=True)                    
            else:
                print("No activities found", end="", flush=True)
                
            print("\nFundings: ", end="", flush=True)
            if record['fundings']['group']:
                for x in record['fundings']['group']:
                    for y in x['funding-summary']:
                        if y['source']['source-name']['value'] == self.source:
                            self.delete_activity("funding", y['put-code'], None)
                            print(y['put-code'],  "", end="", flush=True)
            else:
                print("No activities found", end="", flush=True)
            
            print("\nWorks: ", end="", flush=True)
            if record['works']['group']:
                for x in record['works']['group']:
                    for y in x['work-summary']:
                        if y['source']['source-name']['value'] == self.source:
                            self.delete_activity("work", y['put-code'], None)
                            print (y['put-code'], "", end="", flush=True)
            else:
                print("No activities found", end="", flush=True)

            print("\nPeer reviews: ", end="", flush=True)
            if record['peer-reviews']['group']:
                for x in record['peer-reviews']['group']:
                    for y in x['peer-review-group']:
                        if y['peer-review-summary'][0]['source']['source-name']['value'] == self.source:
                            self.delete_activity("peer-review", y['peer-review-summary'][0]['put-code'], None)
                            print(y['peer-review-summary'][0]['put-code'], "", end="", flush=True)
            else:
                print("No activities found")
                
        except TypeError as e:
            raise (e)       
            
    def logger_setup(self, name, log_file, level=logging.INFO):
        if not os.path.exists("./logs"):
            os.mkdir("./logs")
   
        handler = logging.FileHandler(log_file)                  
        handler.setFormatter(self.formatter)
        
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger 
        
    def orcid_curl(self, url, curl_opts, logger):
        curl_call = ["curl"] + curl_opts + [url]
        while True:
            try:
                p = subprocess.Popen(curl_call, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)                
                output,err = p.communicate()
                if logger is not None:                    
                    logger.info(subprocess.list2cmdline(curl_call))
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
            
            
    def update_xml(self, xml, tag, value, put=False):
        xml = re.sub('put-code=".*?"', '', xml)
        xml = re.sub("<common:external-id-value>(.*?)</common:external-id-value>", "<common:external-id-value>%s</common:external-id-value>" % value, xml)
        if put:
            xml = re.sub('xmlns:common="http://www.orcid.org/ns/common"', 'put-code="%s" xmlns:common="http://www.orcid.org/ns/common"' % value, xml)
        return xml
        
    def update_activity(self, endpoint, putcode, xml, logger):
        xml = self.update_xml(xml, "common:external-id-value", putcode, True)
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + self.access_token, '-H',
                       'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', xml, '-X', 'PUT']
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), curl_params, logger)
        self.assertTrue("<common:external-id-value>%s</common:external-id-value>" % putcode in response, "Putcode %s missing from response: \n" % putcode + response)
    
    def post_activity(self, endpoint, xml, count, logger):
        xml = self.update_xml(xml, "common:external-id-value", count)
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + self.access_token, '-H',
                       'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', xml, '-X', 'POST']
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s" % (self.orcid_id, endpoint), curl_params, logger)
        self.assertTrue("HTTP/1.1 201" in response, "201 code missing from response: \n" + response)
        putcode = self.getputcode(response)        
        return putcode
    
    def delete_activity(self, endpoint, putcode, logger):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % self.access_token, '-H', 'Content-Length: 0', '-H', 'Accept: application/orcid+xml', '-k', '-X', 'DELETE']
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), curl_params, logger)
        self.assertTrue("HTTP/1.1 204" in response, "204 code missing from response: \n" + response)

    def confirmAddedWorks(self, endpoint, putcode, logger):
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), self.curl_params_get, logger)
        self.assertTrue("HTTP/1.1 200" in response, "200 code missing from response: \n" + response)
        
    def confirmUpdatedWorks(self, endpoint, putcode, logger):
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), self.curl_params_get, logger)
        self.assertTrue('"external-id-value":"%s"' % putcode in response, "Putcode %s missing from external identifier in response: \n" % putcode + response)
        
    def confirmRemovedWorks(self, endpoint, putcode, logger):
        response = self.orcid_curl("https://api.qa.orcid.org/v3.0/%s/%s/%s" % (self.orcid_id, endpoint, putcode), self.curl_params_get, logger)
        self.assertTrue("HTTP/1.1 404" in response, "404 code missing from response: \n" + response)
    
    def replicationTest(self, thread_name, endpoint, xml_file):   
        logger = self.logger_setup(endpoint, "./logs/Replication_test_%s.log" % thread_name.lower())
        count = 0
        putcodes = []
        updatedPutcodes = []
        deletedPutcodes = []
        with open("../post_files/" + xml_file, 'r') as file:
            xml = file.read() 
        print("%s: Adding %ss" % (thread_name, endpoint))
        while count < 10:
            putcode = self.post_activity(endpoint, xml, count, logger)
            putcodes.append(putcode)       
            logger.info("%s: %s %s added" % (thread_name, endpoint.capitalize(), putcode))
            count += 1
            
        print("%s: Works added - %s" % (thread_name, putcodes))
        for putcode in putcodes:
            self.confirmAddedWorks(endpoint, putcode, logger)
        print("%s: %s replicas added" % (thread_name, endpoint.capitalize()))        
        updatedPutcodes = random.sample(putcodes, 5)
        print ("%s: Updating %ss - %s" % (thread_name, endpoint, updatedPutcodes))
        for putcode in updatedPutcodes:
            self.update_activity(endpoint, putcode, xml, logger)
            logger.info("%s: %s %s updated" % (thread_name, endpoint.capitalize(), putcode))
        for putcode in updatedPutcodes:
            self.confirmUpdatedWorks(endpoint, putcode, logger)
        print("%s: %s replicas updated" % (thread_name, endpoint.capitalize()))
        deletedPutcodes = random.sample(putcodes, 5)
        print ("%s: Removing %ss - %s" % (thread_name, endpoint, deletedPutcodes))
        for putcode in deletedPutcodes:
            self.delete_activity(endpoint, putcode, logger)
            logger.info("%s: %s %s deleted" % (thread_name, endpoint.capitalize(), putcode))
        for putcode in deletedPutcodes:
            self.confirmRemovedWorks(endpoint, putcode, logger)
        print("%s: %s replicas removed" % (thread_name, endpoint.capitalize()))
        
    def main(self):
        t1 = threading.Thread(target=self.replicationTest, args=("Thread-1", "work", "replication_test_work.xml") )
        t2 = threading.Thread(target=self.replicationTest, args=("Thread-2", "education", "replication_test_edu.xml") )
        t3 = threading.Thread(target=self.replicationTest, args=("Thread-3", "funding", "replication_test_funding.xml") )
        t4 = threading.Thread(target=self.replicationTest, args=("Thread-4", "peer-review", "replication_test_pr.xml") )
        print("Cleaning record...")
        self.cleanup()
        print("Cleaning done")
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        

Replication().main()
