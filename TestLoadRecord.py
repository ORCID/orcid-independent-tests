import unittest
import subprocess

class TestLoadRecord(unittest.TestCase):
    url = 'https://pub.qa.orcid.org/v2.0_rc4/0000-0001-6085-8875C/record'
    response = ''

    def test_read(self):
        p = subprocess.Popen(["curl", self.url,'-H',"Accept: application/json"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output,err = p.communicate()
        self.response = output
        self.assertFalse("error-code" in self.response)