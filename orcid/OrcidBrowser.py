from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import local_properties
import properties

class OrcidBrowser:

    def __init__(self):
        self.server_name = properties.test_server
        self.signin_page = 'https://%s/signin' % self.server_name
        self.auth_page   = 'https://%s/signin/auth.json' % self.server_name
        options = webdriver.FirefoxOptions()
        options.headless = True

        if properties.type == "actions":
            print('------------------------------------------')
            print('Using default firefox and webdriver options')
            print(options)
            print('------------------------------------------')
            self.ff = webdriver.Firefox(options=options)
        else:
            ops = Options()
            
            ops.binary_location = local_properties.firefoxPath
            serv = Service(local_properties.geckodriverPath)
            self.ff = webdriver.Firefox(service=serv, options=ops)

    def bye(self):
        return self.ff.quit()

    def setServerName(self, new_server_name):
        self.server_name = new_server_name

    def getCsrfFrom(self, page):
        self.ff.get(page)
        csrf_meta = self.ff.find_elements_by_name('_csrf')[0]
        csrf_value = csrf_meta.get_attribute('content')
        return csrf_value

    def orcidlogin(self, usrname, secret):
        orcid_record = ''
        try:
            self.ff.get(self.signin_page)
            wait = WebDriverWait(self.ff, 10)
            user_input = wait.until(expected_conditions.presence_of_element_located((By.ID, 'username')))
            user_input.send_keys(usrname)
            pass_input = wait.until(expected_conditions.presence_of_element_located((By.ID, 'password')))
            pass_input.send_keys(secret)
            login_button = wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, (".sign-in-button"))))
            login_button.click()       
            print (usrname)
            print (secret)     
            orcid_found = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'orc-font-heading-small')))
            orcid_record = orcid_found.text
            print ("--- LOGIN OK WITH ID: %s" % orcid_record)
            return str(orcid_record)
        except TimeoutException:
            raise ValueError("failed loading my orcid page.", "orcid: %s" % orcid_record)

    def getImplicitToken(self, usrname, secret, client_id, response_type='token', scope='/authenticate',auth_window = False):
        orcid_record = ''
        oauth_page = 'https://%s/oauth/authorize?client_id=%s&response_type=%s&scope=%s&redirect_uri=https://developers.google.com/oauthplayground&nonce=test' % (self.server_name, client_id, response_type, scope)
        try:
            orcid_record = self.orcidlogin(usrname, secret)
            time.sleep(3)
            self.ff.get(oauth_page)
            wait = WebDriverWait(self.ff, 10)
            try:
                time.sleep(5)
                auth = self.ff.find_element(By.XPATH, '//mat-card-content/button[@mat-raised-button=""]')
                auth.click()
            except Exception:
                print ("Permission already granted")
            button = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'access_token_field')))
            token_input = self.ff.find_element(By.ID, 'for_access_token')
            token_val = token_input.get_attribute('value')
            print ("--- ABOUT TO SEND TOKEN: %s" % token_val)
            return token_val
        except Exception as e:
            print ("Waiting for token failed. url: %s, orcid: %s" % (oauth_page, orcid_record))
            print (e)

    def getAuthCode(self, usrname, secret, client_id, scope='/authenticate',response_type='code',orcid_record='0'):
        oauth_page = 'https://%s/oauth/authorize?client_id=%s&response_type=%s&scope=%s&redirect_uri=https://developers.google.com/oauthplayground' % (self.server_name, client_id,response_type, scope)
        auth_code_val = ''
        try:
            orcid_record = self.orcidlogin(usrname, secret)
            time.sleep(3)
            self.ff.get(oauth_page)
            wait = WebDriverWait(self.ff, 10)
            try:
                time.sleep(5)
                auth = self.ff.find_element(By.XPATH, '//mat-card-content/button[@mat-raised-button=""]')
                auth.click()
            except Exception:
                print ("Permission already granted")
            exchangeCode_button = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'exchangeCode')))
            code_input = self.ff.find_element(By.ID, 'auth_code')
            auth_code_val = code_input.get_attribute('value')
            return auth_code_val
        except Exception as e:
            print("Waiting for auth code failed.", "code: %s | why %s" % (auth_code_val, e))
