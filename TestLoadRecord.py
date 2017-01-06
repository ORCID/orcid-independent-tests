import unittest
import subprocess

class TestLoadRecord(unittest.TestCase):
    
    def orcid_curl(self, url):
        p = subprocess.Popen(["curl", url,'-H',"Accept: application/json", '-i','-k'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output,err = p.communicate()
        return output

    def test_read(self):
        self.response = self.orcid_curl("https://pub.qa.orcid.org/v2.0_rc4/0000-0001-6085-8875/record")
        self.assertFalse("error-code" in self.response, "error-code Not found on json response")
        
    def test_read2(self):
        self.response = self.orcid_curl("https://pub.qa.orcid.org/v2.0_rc4/0000-0001-6085-887X/person")
        self.assertTrue("200 OK" in self.response, "Person not found")
        
    def test_read3(self):
        self.response = self.orcid_curl("https://pub.qa.orcid.org/v2.0_rc4/0000-0001-6085-8875/activities")
        self.assertFalse("404 Not Found" in self.response, "Record not found 404")