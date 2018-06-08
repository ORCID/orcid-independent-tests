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

    def getCsrfFrom(self, page):
        self.ff.get(page)
        csrf_meta = self.ff.find_elements_by_name('_csrf')[0]
        csrf_value = csrf_meta.get_attribute('content')
        self.ff.close()
        return csrf_value

    def login(self, usrname, secret):
        self.ff.get(self.signin_page)
        wait = WebDriverWait(self.ff, 2)
        try:
            user_input = wait.until(expected_conditions.presence_of_element_located((By.ID, 'userId')))
            user_input.send_keys(usrname)
            pass_input = wait.until(expected_conditions.presence_of_element_located((By.ID, 'password')))
            pass_input.send_keys(secret)
            login_button = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'form-sign-in-button')))
            login_button.click()
            orcid_record = wait.until(expected_conditions.presence_of_element_located((By.ID, 'orcid-id')))
            return orcid_record.text
        except TimeoutException:
            print("Waiting for my-orcid page failed.")
        finally:
            self.ff.quit()

    def getToken(self, usrname, secret, client_id):
        try:
            self.ff.get(self.signin_page)
            wait = WebDriverWait(self.ff, 10)
            user_input = wait.until(expected_conditions.presence_of_element_located((By.ID, 'userId')))
            user_input.send_keys(usrname)
            pass_input = wait.until(expected_conditions.presence_of_element_located((By.ID, 'password')))
            pass_input.send_keys(secret)
            login_button = wait.until(expected_conditions.element_to_be_clickable((By.ID, 'form-sign-in-button')))
            login_button.click()
            orcid_record = wait.until(expected_conditions.presence_of_element_located((By.ID, 'orcid-id')))
            #print orcid_record.text
            time.sleep(3)
            oauth_page = 'https://%s/oauth/authorize?client_id=%s&response_type=token&scope=/authenticate&redirect_uri=https://developers.google.com/oauthplayground' % (self.server_name, client_id)
            self.ff.get(oauth_page)
            wait.until(expected_conditions.element_to_be_clickable((By.ID, 'access_token_field')))
            token_input = self.ff.find_element_by_id('for_access_token')
            token_val = token_input.get_attribute('value')
            return token_val
        except TimeoutException:
            print("Waiting for token failed.")
        finally:
            self.ff.quit()
