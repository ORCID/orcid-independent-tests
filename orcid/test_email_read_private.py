import OrcidBaseTest
import pyjavaproperties

class EmailReadPrivate(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
        p = pyjavaproperties.Properties()
        p.load(open('test.properties'))
        self.orcid_props         = p
        self.client_id           = self.orcid_props['memberClientId']
        self.client_secret       = self.orcid_props['memberClientSecret']        
        self.code                = self.orcid_props['emailCode']
        self.orcid_id            = self.orcid_props['orcidId']
        self.access,self.refresh = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
        
    def test_email_scope_not_present(self):
        self.assertIsNotNone(self.access, "No token generated")
        secrets = self.load_secrets_from_file(self.code)
        self.assertTrue('scope' in secrets)
        self.assertFalse("/email/read-private" in secrets.get('scope'), "Unexpected scope returned: " + str(secrets.get('scope')))
