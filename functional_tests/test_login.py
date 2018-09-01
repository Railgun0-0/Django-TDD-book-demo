from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
from .base import FunctionalTest


TEST_EMAIL = 'djangotestmail123@gmail'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertIn('Check your email',
                                            self.browser.find_element_by_tag_name('body').text))

        # a new message in the mail box
        email = mail.outbox[0]
        # mail.outbox function can get the email from server 
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # an url link in mail box
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # click the url
        self.browser.get(url)

        # successfully logged in
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # logging out
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_to_be_logged_out(email=TEST_EMAIL)