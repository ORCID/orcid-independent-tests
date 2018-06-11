from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
import time

class OrcidBrowser:

    def __init__(self):
        self.server_name = 'qa.orcid.org'
        self.signin_page = 'https://%s/signin' % self.server_name
        self.auth_page   = 'https://%s/signin/auth.json' % self.server_name
        self.ff = webdriver.Firefox()

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
            user_input = wait.until(expected_conditions.presence_of_element_located((By.ID, 'userId')))
            user_input.send_keys(usrname)
            pass_input = wait.until(expected_conditions.presence_of_element_located((By.ID, 'password')))
            pass_input.send_keys(secret)
            login_button = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'form-sign-in-button')))
            login_button.click()
            orcid_found = wait.until(expected_conditions.presence_of_element_located((By.ID, 'orcid-id')))
            orcid_record = orcid_found.text
            return orcid_record
        except TimeoutException:
            raise ValueError("failed loading my orcid page.", "orcid: %s" % orcid_record)

    def getImplicitToken(self, usrname, secret, client_id, scope='/authenticate'):
        orcid_record = ''
        oauth_page = 'https://%s/oauth/authorize?client_id=%s&response_type=token&scope=%s&redirect_uri=https://developers.google.com/oauthplayground' % (self.server_name, client_id, scope)
        try:
            orcid_record = self.orcidlogin(usrname, secret)
            time.sleep(3)
            self.ff.get(oauth_page)
            wait = WebDriverWait(self.ff, 10)
            wait.until(expected_conditions.element_to_be_clickable((By.ID, 'access_token_field')))
            token_input = self.ff.find_element_by_id('for_access_token')
            token_val = token_input.get_attribute('value')
            return token_val
        except TimeoutException:
            raise ValueError("Waiting for token failed.", "url: %s" % oauth_page, orcid_record)
