import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class HocamMail:

    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        self.to_inf = None
        self.subject_inf = None
        self.body_inf = None

    def get_mail_template(self):
        try:
            # Open the source for mail template.
            self.driver.get("https://www.hocamclass.com/single-project")
            time.sleep(2)
            self.driver.find_element(By.CSS_SELECTOR, "#comp-l5qf2gr7 > a > div").click()
            time.sleep(2)

            # Get mail template.
            # Get "to" information.
            self.to_inf = self.driver.find_element(By.CSS_SELECTOR, "#comp-l5ptop14 > p > span > span > a").text

            # Get "subject" information (DO NOT WRITE "SUBJECT:").
            self.subject_inf = self.driver.find_element(By.CSS_SELECTOR, "#comp-l5ptpu8a > p > span > span").text

            # Get "body" information (DO NOT WRITE "BODY:").
            self.body_inf = self.driver.find_element(By.CSS_SELECTOR, "#comp-l5ptq8n3 > p > span > span").text
            return True
        except:
            return False

    def login(self, username, password):
        try:
            # Open SquirrelMail service.
            self.driver.get("https://sqrl.metu.edu.tr/src/login.php")
            time.sleep(2)

            # Find the username field and send the username.
            username_area = self.driver.find_element(By.NAME, "login_username")
            username_area.send_keys(username)
            time.sleep(2)

            # Find the password field and send the password.
            password_area = self.driver.find_element(By.NAME, "secretkey")
            password_area.send_keys(password)
            time.sleep(2)

            # Find the login button and click
            login_button = self.driver.find_element(By.CSS_SELECTOR, "body > form > table > tbody > tr > td > center > "
                                                                     "table > tbody > tr:nth-child(3) > td > center > "
                                                                     "input[type=submit]")
            login_button.click()
            time.sleep(5)
            return True
        except:
            return False

    def send_mail_template(self):
        try:
            # Open new mail page.
            self.driver.get("https://sqrl.metu.edu.tr/src/compose.php?mailbox=INBOX&startMessage=1")
            time.sleep(2)

            # Fill "to" section
            to_slot = self.driver.find_element(By.NAME, "send_to")
            to_slot.send_keys(self.to_inf)

            # Fill "subject" section
            subject_slot = self.driver.find_element(By.NAME, "subject")
            subject_slot.send_keys(self.subject_inf)

            # Fill the body
            body_slot = self.driver.find_element(By.NAME, "body")
            body_slot.send_keys(self.body_inf)

            # Find the "send" key and send the mail
            self.driver.find_element(By.NAME, "body").click()
            return True
        except:
            return False
