from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class UserJourneyTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        cls.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_user_register_and_review(self):
        browser = self.browser

        browser.get(self.live_server_url)
        time.sleep(1)

        browser.find_element(By.LINK_TEXT, "Get Started").click()
        time.sleep(1)

        browser.find_element(By.NAME, "username").send_keys("user")
        browser.find_element(By.NAME, "email").send_keys("user@exmaple.com")
        browser.find_element(By.NAME, "password1").send_keys("PIDor__123")
        browser.find_element(By.NAME, "password2").send_keys("PIDor__123")
        browser.find_element(By.TAG_NAME, "form").submit()
        time.sleep(1)

        

        