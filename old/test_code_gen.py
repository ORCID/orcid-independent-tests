import OrcidBaseTest
import properties

class CodeGen(OrcidBaseTest.OrcidBaseTest):
    
    def setUp(self):
        self.scope = "/authenticate"
        self.code  = self.generate_auth_code(properties.publicClientId,self.scope)
        #print self.code
        self.access = None
        self.refresh = None
        if str(self.code):
            self.access,self.refresh = self.orcid_exchange_auth_token(properties.publicClientId,properties.publicClientSecret,self.code)

    def test_post_work(self):
        self.assertIsNotNone(self.code,"Code=[%s] " % (self.code))
        self.assertIsNotNone(self.access,"Access[%s]" % (self.access))
        
