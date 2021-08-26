import OrcidBaseTest
import properties
import local_properties

class PrivateRecord(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        if properties.type == "actions":
          self.test_server = properties.test_server
        else:
          self.test_server = local_properties.test_server
        self.public_token = 'ba290a09-b757-4583-a5af-bd55d7087467'
        self.public_api_token = '80e4aa5a-6ccc-44b3-83bb-3d9e315cda22'
        self.private_orcid_id = '0000-0003-2366-2712'
        self.limited_token = '6ae41a5b-abf9-4922-bbb4-08ed8508b4ce'
        self.empty_activities = '"orcid-activities":null'
        self.empty_bio = '"orcid-bio":null'
        self.empty_email = '"email":[]'
        self.activities = ['educations', 'employments', 'fundings', 'works', 'peer-reviews']
        self.bio_sections2 = ['other-name', 'researcher-url', 'keyword', 'external-identifier', 'email', 'address']

    def test_read_private_record_with_20_public_api(self):
    #Test reading a private record with the 2.0 api and public token
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + properties.test_server + "/v2.0/" + self.private_orcid_id + "/record", curl_params)
    #Check the name and email address are not returned anywhere
      self.assertFalse('Published Name' in response, "Name returned " + response)
      self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
    #Check each bio and activities section is returned without content
      for bio_section in self.bio_sections2:
        if bio_section == 'email':
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        elif bio_section == 'address':
          self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        else:
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
      for activity in self.activities:
        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

    def test_read_private_record_with_21_public_api(self):
      #Test reading a private record with the 2.1 api
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v2.1/" + self.private_orcid_id + "/record", curl_params)
      #Check the name and email address are not returned anywhere
      self.assertFalse('Published Name' in response, "Name returned " + response)
      self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
      #Check each bio and activities section is returned without content
      for bio_section in self.bio_sections2:
        if bio_section == 'email':
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        elif bio_section == 'address':
          self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        else:
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
      for activity in self.activities:
        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

    def test_read_private_record_with_30_rc1_public_api(self):
      #Test reading a private record with the 3.0 api and public token
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc1/" + self.private_orcid_id + "/record", curl_params)
      #Check the name and email address are not returned anywhere
      self.assertFalse('Published Name' in response, "Name returned " + response)
      self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
      #Check each bio and activities section is returned without content
      for bio_section in self.bio_sections2:
        if bio_section == 'email':
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        elif bio_section == 'address':
          self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        else:
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
      for activity in self.activities:
        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

    def test_read_private_record_with_30_rc2_public_api(self):
      # Test reading a private record with the 3.0 api and public token
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L','-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc2/" + self.private_orcid_id + "/record", curl_params)
      # Check the name and email address are not returned anywhere
      self.assertFalse('Published Name' in response, "Name returned " + response)
      self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
      # Check each bio and activities section is returned without content
      for bio_section in self.bio_sections2:
        if bio_section == 'email':
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response,"Non-empty section " + bio_section + response)
        elif bio_section == 'address':
          self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response,"Non-empty section " + bio_section + response)
        else:
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response,"Non-empty section " + bio_section + response)
      for activity in self.activities:
        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response,"Non-empty section " + activity + response)

    def test_read_private_record_with_30_public_api(self):
      # Test reading a private record with the 3.0 api and public token
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L','-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v3.0/" + self.private_orcid_id + "/record", curl_params)
      # Check the name and email address are not returned anywhere
      self.assertFalse('Published Name' in response, "Name returned " + response)
      self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
      # Check each bio and activities section is returned without content
      for bio_section in self.bio_sections2:
        if bio_section == 'email':
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response,"Non-empty section " + bio_section + response)
        elif bio_section == 'address':
          self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response,"Non-empty section " + bio_section + response)
        else:
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response,"Non-empty section " + bio_section + response)
      for activity in self.activities:
        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response,"Non-empty section " + activity + response)

    def test_read_private_record_with_20_limited_token(self):
      #Test reading a private record with 2.0 api and a limited token
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.private_orcid_id + "/record", curl_params)
      #Check the name and email address are not returned anywhere
      self.assertFalse('Published Name' in response, "Name returned " + response)
      self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
      #Check each bio and activities section is returned without content
      for bio_section in self.bio_sections2:
        if bio_section == 'email':
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        elif bio_section == 'address':
          self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        else:
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
      for activity in self.activities:
        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

    def test_read_private_record_with_21_limited_token(self):
      #Test reading a private record with a 2.1 api and limited token check no private information is returned
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.private_orcid_id + "/record", curl_params)
      #Check the name and email address are not returned anywhere
      self.assertFalse('Published Name' in response, "Name returned " + response)
      self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
      #Check each bio and activities section is returned without content
      for bio_section in self.bio_sections2:
        if bio_section == 'email':
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        elif bio_section == 'address':
          self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        else:
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
      for activity in self.activities:
        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

    def test_read_private_record_with_30_rc1_limited_token(self):
      #Test reading a private record with a 3.0 api and limited token check no private information is returned
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.private_orcid_id + "/record", curl_params)
      #Check the name and email address are not returned anywhere
      self.assertFalse('Published Name' in response, "Name returned " + response)
      self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
      #Check each bio and activities section is returned without content
      for bio_section in self.bio_sections2:
        if bio_section == 'email':
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        elif bio_section == 'address':
          self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        else:
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
      for activity in self.activities:
        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

    def test_read_private_record_with_30_rc2_limited_token(self):
      #Test reading a private record with a 3.0 api and limited token check no private information is returned
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.private_orcid_id + "/record", curl_params)
      #Check the name and email address are not returned anywhere
      self.assertFalse('Published Name' in response, "Name returned " + response)
      self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
      #Check each bio and activities section is returned without content
      for bio_section in self.bio_sections2:
        if bio_section == 'email':
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        elif bio_section == 'address':
          self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        else:
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
      for activity in self.activities:
        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

    def test_read_private_record_with_30_limited_token(self):
      #Test reading a private record with a 3.0 api and limited token check no private information is returned
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.private_orcid_id + "/record", curl_params)
      #Check the name and email address are not returned anywhere
      self.assertFalse('Published Name' in response, "Name returned " + response)
      self.assertFalse('private_ma@mailinator.com' in response, "Email returned " + response)
      #Check each bio and activities section is returned without content
      for bio_section in self.bio_sections2:
        if bio_section == 'email':
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        elif bio_section == 'address':
          self.assertTrue('<' + bio_section + ':' + bio_section + 'es path="/' + self.private_orcid_id + '/' + bio_section + '"/>' in response, "Non-empty section " + bio_section + response)
        else:
          self.assertTrue('<' + bio_section + ':' + bio_section + 's path="/' + self.private_orcid_id + '/' + bio_section + 's"/>' in response, "Non-empty section " + bio_section + response)
      for activity in self.activities:
        self.assertTrue('<activities:' + activity + ' path="/' + self.private_orcid_id + '/' + activity + '"/>' in response, "Non-empty section " + activity + response)

    def test_read_private_work_with_20_limited_token(self):
        #Test reading a private work with a 2.0 api and limited token check no private information is returned
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.private_orcid_id + "/work/141943", curl_params)
        self.assertTrue("<error-code>9013</error-code>" in response, "Expected error code 9013 instead: " + response)

    def test_read_private_email_with_20_limited_token(self):
        #Test reading a private email with a 2.0 api and limited token check no private information is returned
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/" + self.private_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_deactivated_record_member_api_20(self):
    #Test reading a deactivated record with member 2.0 api and check a deactivated date is returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/0000-0002-7564-3444/record", curl_params)
        response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2].strip().replace(self.test_server, "qa.orcid.org")
        #Check record has deactivated date
        saved_file = open('saved_records/deactivated_record20.xml','r').read()
        self.assertTrue(response_body == saved_file, "No deactivate date " + response_body +
        "\nSaved file: " + saved_file)

    def test_read_deactivated_record_public_api_20(self):
    #Test reading a deactivated record with public 2.0 api and check a deactivated date is returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.0/0000-0002-7564-3444/record", curl_params)
        response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2].strip().replace(self.test_server, "qa.orcid.org")
        #Check record has deactivated date
        saved_file = open('saved_records/deactivated_record20.xml','r').read()
        self.assertTrue(response_body == saved_file, "No deactivate date " + response_body + "\nSaved file: " + saved_file)

    def test_read_locked_record_member_api_20(self):
    #Test reading a locked record with member 2.0 api and check a deactivated date is returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/0000-0002-1871-711X/record", curl_params)
        #Check locked error is returned
        self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_locked_record_public_api_20(self):
    #Test reading a locked record with public 2.0 api and check a locked error is returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.0/0000-0002-1871-711X/record", curl_params)
        #Check locked error is returned
        self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_deprecated_record_member_api_20(self):
    #Test reading a deprecated record with public 2.0 api and check a deactivated date is returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.0/0000-0003-2914-7527/record", curl_params)
        #Check locked error is returned
        self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

    def test_read_deprecated_record_public_api_20(self):
    #Test reading a deprecated record with public 2.0 api and check a 9007 error is returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.0/0000-0003-2914-7527/record", curl_params)
        #Check locked error is returned
        self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

#2.1 tests

    def test_read_private_work_with_21_limited_token(self):
        #Test reading a private work with a 2.1 api and limited token check no private information is returned
        curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.private_orcid_id + "/work/141943", curl_params)
        self.assertTrue("<error-code>9013</error-code>" in response, "Expected error code 9013 instead: " + response)

    def test_read_private_email_with_21_limited_token(self):
        #Test reading a private email with a 2.1 api and limited token check no private information is returned
        curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/" + self.private_orcid_id + "/email", curl_params)
        #Check an empty email sections is returned
        self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_deactivated_record_member_api_21(self):
    #Test reading a deactivated record with member 2.1 api and check a deactivated date is returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/0000-0002-7564-3444/record", curl_params)
        response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2].strip().replace(self.test_server, "qa.orcid.org")
        #Check record has deactivated date
        saved_file = open('saved_records/deactivated_record21.xml','r').read()
        self.assertTrue(response_body == saved_file, "No deactivate date " + response_body + "\nSaved file: " + saved_file)

    def test_read_deactivated_record_public_api_21(self):
    #Test reading a deactivated record with public 2.1 api and check a deactivated date is returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.1/0000-0002-7564-3444/record", curl_params)
        response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2].strip().replace(self.test_server, "qa.orcid.org")
        #Check record has deactivated date
        saved_file = open('saved_records/deactivated_record21.xml','r').read()
        self.assertTrue(response_body == saved_file, "No deactivate date " + response_body + "\nSaved file: " + saved_file)

    def test_read_locked_record_member_api_21(self):
    #Test reading a locked record with member 2.1 api and check a locked error is returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://api." + self.test_server + "/v2.1/0000-0002-1871-711X/record", curl_params)
        #Check locked error is returned
        self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_locked_record_public_api_21(self):
      #Test reading a locked record with public 2.1 api and check a locked error is returned
        curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
        response = self.orcid_curl("https://pub." + self.test_server + "/v2.1/0000-0002-1871-711X/record", curl_params)
        #Check locked error is returned
        self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_deprecated_record_member_api_21(self):
    #Test reading a deprecated record with member 2.1 api and check an 9007 error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v2.1/0000-0003-2914-7527/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

    def test_read_deprecated_record_public_api_21(self):
    #Test reading a deprecated record with public 2.1 api and check an 9007 error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v2.1/0000-0003-2914-7527/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

#3.0 rc1 tests

    def test_read_private_work_with_30_rc1_limited_token(self):
      #Test reading a private work with a 3.0_rc1 api and limited token check no private information is returned
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.private_orcid_id + "/work/141943", curl_params)
      self.assertTrue("<error-code>9013</error-code>" in response, "Expected error code 9013 instead: " + response)

    def test_read_private_email_with_30_rc1_limited_token(self):
      #Test reading a private email with a 3.0_rc1 api and limited token check no private information is returned
      curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/" + self.private_orcid_id + "/email", curl_params)
      #Check an empty email sections is returned
      self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_deactivated_record_member_api_30_rc1(self):
    #Test reading a deactivated record with member 3.0_rc1 api and check a deactivated date is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/0000-0002-7564-3444/record", curl_params)
      response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2].strip().replace(self.test_server, "qa.orcid.org")
      #Check record has deactivated date
      self.assertTrue(response_body == open('saved_records/deactivated_record30_rc1.xml','r').read(), "No deactivate date " + response_body)

    def test_read_deactivated_record_public_api_30_rc1(self):
    #Test reading a deactivated record with public 3.0_rc1 api and check a deactivated date is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc1/0000-0002-7564-3444/record", curl_params)
      response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2].strip().replace(self.test_server, "qa.orcid.org")
      #Check record has deactivated date
      self.assertTrue(response_body == open('saved_records/deactivated_record30_rc1.xml','r').read(), "No deactivate date " + response_body)

    def test_read_locked_record_member_api_30_rc1(self):
    #Test reading a locked record with member 3.0_rc1 api and check a locked error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/0000-0002-1871-711X/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_locked_record_public_api_30_rc1(self):
    #Test reading a locked record with public 3.0_rc1 api and check a locked error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc1/0000-0002-1871-711X/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_deprecated_record_member_api_30_rc1(self):
    #Test reading a deprecated record with member 3.0_rc1 api and check an 9007 error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc1/0000-0003-2914-7527/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

    def test_read_deprecated_record_public_api_30_rc1(self):
    #Test reading a deprecated record with public 3.0_rc1 api and check an 9007 error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc1/0000-0003-2914-7527/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

#3.0 rc2 tests

    def test_read_private_work_with_30_rc2_limited_token(self):
      #Test reading a private work with a 3.0_rc2 api and limited token check no private information is returned
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.private_orcid_id + "/work/141943", curl_params)
      self.assertTrue("<error-code>9013</error-code>" in response, "Expected error code 9013 instead: " + response)

    def test_read_private_email_with_30_rc2_limited_token(self):
      #Test reading a private email with a 3.0_rc2 api and limited token check no private information is returned
      curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/" + self.private_orcid_id + "/email", curl_params)
      #Check an empty email sections is returned
      self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_deactivated_record_member_api_30_rc2(self):
    #Test reading a deactivated record with member 3.0_rc2 api and check a deactivated date is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/0000-0002-7564-3444/record", curl_params)
      response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2].strip().replace(self.test_server, "qa.orcid.org")
      #Check record has deactivated date
      saved_file = open('saved_records/deactivated_record30_rc2.xml','r').read()
      self.assertTrue(response_body == saved_file, "No deactivate date " + response_body + "\nSaved file: " + saved_file)

    def test_read_deactivated_record_public_api_30_rc2(self):
    #Test reading a deactivated record with public 3.0_rc2 api and check a deactivated date is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc2/0000-0002-7564-3444/record", curl_params)
      response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2].strip().replace(self.test_server, "qa.orcid.org")
      #Check record has deactivated date
      saved_file = open('saved_records/deactivated_record30_rc2.xml','r').read()
      self.assertTrue(response_body == saved_file, "No deactivate date " + response_body + "\nSaved file: " + saved_file)

    def test_read_locked_record_member_api_30_rc2(self):
    #Test reading a locked record with member 3.0_rc2 api and check a locked error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/0000-0002-1871-711X/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_locked_record_public_api_30_rc2(self):
    #Test reading a locked record with public 3.0_rc1 api and check a locked error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc2/0000-0002-1871-711X/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_deprecated_record_member_api_30_rc2(self):
    #Test reading a deprecated record with member 3.0_rc1 api and check an 9007 error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0_rc2/0000-0003-2914-7527/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

    def test_read_deprecated_record_public_api_30_rc2(self):
    #Test reading a deprecated record with public 3.0_rc2 api and check an 9007 error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v3.0_rc2/0000-0003-2914-7527/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

#3.0 tests

    def test_read_private_work_with_30_limited_token(self):
      #Test reading a private work with a 3.0 api and limited token check no private information is returned
      curl_params = ['-H', "Accept: application/xml", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.private_orcid_id + "/work/141943", curl_params)
      self.assertTrue("<error-code>9013</error-code>" in response, "Expected error code 9013 instead: " + response)

    def test_read_private_email_with_30_limited_token(self):
      #Test reading a private email with a 3.0 api and limited token check no private information is returned
      curl_params = ['-H', "Accept: application/json", '-H', 'Authorization: Bearer ' + self.limited_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0/" + self.private_orcid_id + "/email", curl_params)
      #Check an empty email sections is returned
      self.assertTrue(self.empty_email in response, "Non-empty email returned " + response)

    def test_read_deactivated_record_member_api_30(self):
    #Test reading a deactivated record with member 3.0 api and check a deactivated date is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0/0000-0002-7564-3444/record", curl_params)
      response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2].strip().replace(self.test_server, "qa.orcid.org")
      #Check record has deactivated date
      saved_file = open('saved_records/deactivated_record30.xml','r').read()
      self.assertTrue(response_body == saved_file, "No deactivate date " + response_body + "\nSaved file: " + saved_file)

    def test_read_deactivated_record_public_api_30(self):
    #Test reading a deactivated record with public 3.0 api and check a deactivated date is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v3.0/0000-0002-7564-3444/record", curl_params)
      response_body = response.partition('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')[2].strip().replace(self.test_server, "qa.orcid.org")
      #Check record has deactivated date
      saved_file = open('saved_records/deactivated_record30.xml','r').read()
      self.assertTrue(response_body == saved_file, "No deactivate date " + response_body + "\nSaved file: " + saved_file)

    def test_read_locked_record_member_api_30(self):
    #Test reading a locked record with member 3.0 api and check a locked error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0/0000-0002-1871-711X/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_locked_record_public_api_30(self):
    #Test reading a locked record with public 3.0 api and check a locked error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-L', '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v3.0/0000-0002-1871-711X/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9018</error-code>" in response, "Locked message not returned " + response)

    def test_read_deprecated_record_member_api_30(self):
    #Test reading a deprecated record with member 3.0 api and check an 9007 error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_token, '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://api." + self.test_server + "/v3.0/0000-0003-2914-7527/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

    def test_read_deprecated_record_public_api_30(self):
    #Test reading a deprecated record with public 3.0 api and check an 9007 error is returned
      curl_params = ['-H', "Accept: application/orcid+xml", '-H', 'Authorization: Bearer ' + self.public_api_token, '-i', '-k', '-X', 'GET']
      response = self.orcid_curl("https://pub." + self.test_server + "/v3.0/0000-0003-2914-7527/record", curl_params)
      #Check locked error is returned
      self.assertTrue("<error-code>9007</error-code>" in response, "Deactivated message not returned " + response)

