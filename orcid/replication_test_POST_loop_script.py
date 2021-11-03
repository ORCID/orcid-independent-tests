#!/usr/bin/env python3
import subprocess
import re
import os
import time
import json
import unittest
import random
import threading
import logging
import argparse
import yaml
import xml.dom.minidom as md

class Replication(unittest.TestCase):
    ''' Stdout formatting:
    +++ +++ Added activities/replicas are surrounded by plus signs 
    ((( ))) Updated activities/replicas are surrounded by parentheses
    --- --- Removed activities/replicas are surrounded by minus signs
    '''
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--config', help='yaml config file', required=True)
        args = parser.parse_args()
        path = args.config
    
        with open(path) as file:
            params = yaml.load(file, Loader=yaml.FullLoader)
        self.confirm = params['confirm']
        self.test_server = params['test_server']
        self.replication_server = params['replication_server']
        self.protocol = params['protocol']
        self.number_of_activities = params['number_of_activities']
        self.number_of_activities_sample = params['number_of_activities_sample']        
        self.quick_replication_limit = params['quick_replication_limit']        
        self.orcid_id = params['orcid_id']
        self.access_token = params['access_token']     
        self.source = params['source']
        
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.curl_params_get = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % self.access_token, '-H', 'Content-Length: 0', '-H', 'Accept: application/json', '-k', '-X', 'GET']                        
                        
    def orcid_curl(self, url, curl_opts, logger):
        curl_call = ["curl"] + curl_opts + [url]
        while True:
            try:
                p = subprocess.Popen(curl_call, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)                
                output,err = p.communicate()                
                return output.decode()
            except Exception as e:
                raise Exception(e)
            break
            
    def getputcode(self, post_response):
        putcode = ''
        for header in post_response.split('\n'):
            if("location:" in header.lower()):
                location_chunks = header.split('/')
                putcode = location_chunks[-1].strip()
        return putcode
            
            
    def update_xml(self, xml, tag, value, put=False):
        xml = re.sub('put-code=".*?"', '', xml)
        xml = re.sub("<common:external-id-value>(.*?)</common:external-id-value>", "<common:external-id-value>%s</common:external-id-value>" % value, xml)
        if put:
            xml = re.sub('xmlns:common="http://www.orcid.org/ns/common"', 'put-code="%s" xmlns:common="http://www.orcid.org/ns/common"' % value, xml)
        return xml            
    
    def post_activity(self, endpoint, xml, count, logger, verify=False):
        xml = self.update_xml(xml, "common:external-id-value", count)
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + self.access_token, '-H',
                       'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', xml, '-X', 'POST']
        response = self.orcid_curl("https://api.%s/v3.0/%s/%s" % (self.test_server, self.orcid_id, endpoint), curl_params, logger)
        self.assertTrue(self.protocol + " 201" in response, "201 code missing from response: \n" + response)
        putcode = self.getputcode(response)
        # Verify makes the process too slow
        # if verify:
        #    time.sleep(0.01)
        #    response = self.orcid_curl("https://api.%s/v3.0/%s/%s/%s" % (self.replication_server, self.orcid_id, endpoint, putcode), self.curl_params_get, logger)
        #    self.assertTrue(self.protocol + " 200" in response, "200 code missing from response: \n" + response)
        # Return put code
        return putcode
    
    def update_activity(self, endpoint, putcode, xml, logger, verify=False):
        xml = self.update_xml(xml, "common:external-id-value", putcode, True)
        curl_params = ['-i', '-L', '-H', 'Authorization: Bearer ' + self.access_token, '-H',
                       'Content-Type: application/orcid+xml', '-H', 'Accept: application/xml', '-d', xml, '-X', 'PUT']
        response = self.orcid_curl("https://api.%s/v3.0/%s/%s/%s" % (self.test_server, self.orcid_id, endpoint, putcode), curl_params, logger)
        self.assertTrue("<common:external-id-value>%s</common:external-id-value>" % putcode in response, "Putcode %s missing from response: \n" % putcode + response)        
        # Verify makes the process too slow
        # if verify:
        #    time.sleep(0.01)
        #    response = self.orcid_curl("https://api.%s/v3.0/%s/%s/%s" % (self.replication_server, self.orcid_id, endpoint, putcode), self.curl_params_get, logger)
        #    self.assertTrue('"external-id-value":"%s"' % putcode in response, "Putcode %s missing from external identifier in response: \n" % putcode + response)

    def delete_activity(self, endpoint, putcode, logger):
        curl_params = ['-L', '-i', '-k', '-H', 'Authorization: Bearer %s' % self.access_token, '-H', 'Content-Length: 0', '-H', 'Accept: application/orcid+xml', '-k', '-X', 'DELETE']
        response = self.orcid_curl("https://api.%s/v3.0/%s/%s/%s" % (self.test_server, self.orcid_id, endpoint, putcode), curl_params, logger)
        self.assertTrue(self.protocol + " 204" in response, "204 code missing from response: \n" + response)
        time.sleep(0.010)
        # Verify makes the process too slow
        # response = self.orcid_curl("https://api.%s/v3.0/%s/%s/%s" % (self.replication_server, self.orcid_id, endpoint, putcode), self.curl_params_get, logger)
        # self.assertTrue(self.protocol + " 404" in response, "404 code missing from response: \n" + response)        
        
    def main(self):
        # Log config 
        if not os.path.exists("./logs"):
            os.makedirs("./logs", exist_ok=True)       
        handler = logging.FileHandler("./logs/progress.log")                  
        handler.setFormatter(self.formatter)
        
        logger = logging.getLogger("progress")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        # Variables
        endpoint = "work"
        workXml = ''
        # Random value to start the index count, make it crazy big so it is less likely it will match any other existing value
        index = random.random() * 100000000
        putcodes = []        

        with open("../post_files/replication_test_work.xml", 'r') as file:
            workXml = file.read()

        while True:
            # POST work
            putcode = self.post_activity(endpoint, workXml, index, logger)
            logger.info("POST %s" % (putcode))
            # Save put code
            putcodes.append(putcode)
            # Increment index
            index += 1
            # Randomly update an entry 10% of the iterations
            if random.random() < 0.1:
                putcode_to_update = random.choice(putcodes)
                logger.info("Trying to update %s" % (putcode))
                self.update_activity(endpoint, putcode_to_update, workXml, logger)
                logger.info("PUT %s" % (putcode))
            # Randomly delete an entry 5% of the iterations
            if random.random() < 0.05:
                putcode_to_delete = random.choice(putcodes)
                logger.info("Trying to delete %s" % (putcode))
                self.delete_activity(endpoint, putcode_to_delete, logger)
                logger.info("DELETE %s" % (putcode))
                # Remove this from the list of put codes so it is not updated nor deleted again
                putcodes.remove(putcode)

Replication().main()
