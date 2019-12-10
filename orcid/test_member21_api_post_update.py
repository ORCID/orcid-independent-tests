import OrcidBaseTest
import properties
import local_properties

class Member20ApiPostUpdate(OrcidBaseTest.OrcidBaseTest):

    def setUp(self):
      self.version = "/v2.1/"
      if local_properties.type == "jenkins":
        self.client_id     = properties.memberClientId
        self.client_secret = properties.memberClientSecret
        self.notify_token  = properties.notifyToken
        self.orcid_id      = properties.orcidId
        self.scope               = "openid"
        self.code                = self.generate_auth_code(self.client_id,self.scope, "OpenIDCode")
        self.access,self.refresh,self.id_token = self.orcid_exchange_auth_token(self.client_id,self.client_secret,self.code)
        print "Using code: %s | access: %s " % (self.code, self.access)
      else:
        self.orcid_id = local_properties.orcid_id_member
        self.access = local_properties.access_member
        self.notify_token = local_properties.notify_token
    

        
        
