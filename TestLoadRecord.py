import junit_xml
import subprocess
import unittest

class TestLoadRecord(unittest.TestCase):
    url = 'https://pub.qa.orcid.org/v2.0_rc4/0000-0001-6085-8875/record'
    response = ''
    
    def test_read(self):
        p = subprocess.Popen(["curl", self.url,'-H',"Accept: application/json"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output,err = p.communicate()
        self.assertFalse("error-code" in self.response)

test_cases = [junit_xml.TestCase('TestLoadRecord',TestLoadRecord)]
ts = junit_xml.TestSuite("API Manual Tests", test_cases)
print(junit_xml.TestSuite.to_xml_string([ts]))
