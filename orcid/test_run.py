import OrcidBaseTest
import properties

class Run(OrcidBaseTest.OrcidBaseTest):
    
    def setUp(self):
        self.scope = "/authenticate"
        self.code  = self.generate_auth_code(properties.publicClientId,self.scope)
        print self.code
        self.access = None
        self.refresh = None
        #if str(self.code):
            #self.access,self.refresh = self.orcid_exchange_auth_token(properties.publicClientId,properties.publicClientSecret,self.code)

    def test_post_work(self):
        self.assertNotNone(self.access,"Code=[%s] and access[%s]" % (str(self.code),str(self.access)))
        
