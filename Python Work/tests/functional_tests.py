from selenium import webdriver
import unittest

class TestUserFunctionality(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_page_loads_correctly(self):
        self.browser.get("http:\\localhost")
        self.assertIn("Botender", self.browser.title, "Page did not load correctly.")

    def tearDown(self):
        self.browser.close()


if __name__ == '__main__':
    unittest.main()
