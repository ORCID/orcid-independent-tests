import OrcidBaseTest
import testinputs

class Run(OrcidBaseTest.OrcidBaseTest):
    
    def setUp(self):
        self.scope = "/authenticate"
        self.code  = self.generate_auth_code(testinputs.publicClientId,self.scope)
        self.access = None
        self.refresh = None
        if str(self.code):
            self.access,self.refresh = self.orcid_exchange_auth_token(testinputs.publicClientId,testinputs.publicClientSecret,self.code)

    def test_post_work(self):
        self.assertTrue(False,"Code=[%s] and access[%s]" % (str(self.code),str(self.access)))
        
