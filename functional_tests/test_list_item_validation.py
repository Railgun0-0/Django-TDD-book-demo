from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # enter nothing to the input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # indicates an error of the empty input
        # self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.has-error').text,
        #                  "You can't have an empty list item"))

        # browser block the request. List will not show
        self.wait_for(lambda: self.browser.find_element_by_css_selector('#id_text:invalid'))

        # enter some texts and submit this time is ok
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:valid'))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        self.get_item_input_box().send_keys(Keys.ENTER)

        # browser block the empty input again
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))

        # enter some text. And this will be fine
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')

        # enter the duplicate text by accident
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(self.get_error_element().text,
                                               "You've already got this in your list"))

    def test_error_messages_are_cleared_on_input(self):
        # make a new list but something wrong
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # in order to get rid of the mistake, enter the correct input
        self.get_item_input_box().send_keys('a')

        # this time it does not show the error message
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))