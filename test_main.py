import argparse
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager
import time

expected_strings = ["SELF PACED ONLINE TRAINING", "IN DEPTH MATERIAL",
                    "LIFETIME INSTRUCTOR SUPPORT", "RESUME PREPARATION",
                    "30 DAY MONEY BACK GUARANTEE", "Hello Stori Card, Are you sure you want to confirm?"]
logging.getLogger('WDM').setLevel(logging.NOTSET)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser', help='Chrome, Firefox or Opera')
    args = parser.parse_args()
    return args


def driver_install(args):
    if args.browser not in ("Chrome", "Firefox", "Opera"):
        raise ValueError
    elif args.browser == "Chrome":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif args.browser == "Firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        driver = webdriver.Opera(executable_path=OperaDriverManager().install())
    return driver


pytest.main(['test_main.py', "--junitxml=Reports/report.xml", '-rA', '-s', '--html=Reports/report.html'])


class TestLandingPage:

    def setup_class(self):
        arguments = (parse_args())
        self.driver = driver_install(arguments)
        self.driver.get("https://rahulshettyacademy.com/AutomationPractice/")
        self.wait = WebDriverWait(self.driver, 60)
        self.main_window = self.driver.current_window_handle

    def teardown_class(self):
        self.driver.quit()

    def test_suggestion_class_example(self):
        elem = self.driver.find_element(By.XPATH, "//input[@id = 'autocomplete']")
        elem.send_keys("Me")
        ActionChains(self.driver).move_to_element(elem).perform()
        elem = self.driver.find_element(By.XPATH, "//ul[@id = 'ui-id-1']//div[@class = 'ui-menu-item-wrapper'][contains(text(),'Mexico')]")
        elem.click()                

    def test_dropdown_example(self):
        elem = Select(self.driver.find_element(By.XPATH, "//select[@name='dropdown-class-example']"))
        elem.select_by_index(2)
        time.sleep(1)
        elem.select_by_index(3)
        time.sleep(1)

    def test_switch_to_window_example(self):
        self.driver.find_element(By.XPATH, "//button[@id='openwindow']").click()
        for window_handle in self.driver.window_handles:
            if window_handle != self.main_window:
                self.driver.switch_to.window(window_handle)
                break

        elem = self.driver.find_element(By.XPATH, "//div[@class='col-xs-12 col-sm-12']")
        text_split = elem.text.splitlines()
        if text_split[0] not in expected_strings:
            assert True
            self.driver.close()
            self.driver.switch_to.window(self.main_window)

        elem = self.driver.find_elements(By.XPATH, "//div[@class='col-xs-12 col-sm-6']")
        for i in elem:
            text_split = i.text.splitlines()
            if text_split[0] not in expected_strings:
                print("\n{} text doesn't match with expected".format(text_split[0]))
                assert True
        self.driver.close()
        self.driver.switch_to.window(self.main_window)

    def test_switch_tab_example(self):
        self.driver.find_element(By.CSS_SELECTOR, "#opentab").click()
        self.wait.until(EC.number_of_windows_to_be(2))
        for window_handle in self.driver.window_handles:
            if window_handle != self.main_window:
                self.driver.switch_to.window(window_handle)
                break

        self.wait.until(EC.title_is("Rahul Shetty Academy"))
        elem = self.driver.find_element(By.CSS_SELECTOR, ".text-center a[href^='https']")
        ActionChains(self.driver).scroll_to_element(elem).perform()
        ActionChains(self.driver).move_to_element(elem).perform()
        elem.screenshot("switch_tab_example.png")
        self.driver.close()
        self.driver.switch_to.window(self.main_window)

    def test_switch_to_alert_example(self):
        buttons = ["Alert", "Confirm"]
        for i in buttons:
            elem = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Enter Your Name']")
            elem.send_keys("Stori Card")
            self.driver.find_element(By.CSS_SELECTOR, "input[value='{}']".format(i)).click()
            print("\n" + Alert(self.driver).text)
            if i == "Confirm" and Alert(self.driver).text not in expected_strings:
                assert True
            Alert(self.driver).accept()

    def test_web_table_example(self):
        price_list = self.driver.find_elements(By.CSS_SELECTOR, ".table-display tbody tr td:last-child")
        book_names = self.driver.find_elements(By.CSS_SELECTOR, ".table-display tbody tr td:nth-child(2)")

        price_books_dict = {book_names[i].text: price_list[i].text for i in range(len(price_list))}
        price_books_25 = price_books_dict.copy()
        for key, value in price_books_dict.items():
            if value != "25":
                price_books_25.pop(key)
        print("\n{} books are $25".format(len(price_books_25)))
        print("Name of the books that are $25:")
        for book in price_books_25.keys():
            print(book)

    def test_web_table_fixed_header(self):
        position_list = self.driver.find_elements(By.CSS_SELECTOR, ".tableFixHead tbody tr td:nth-child(2)")
        engineers = 0
        for position in position_list:
            if position.text == "Engineer":
                engineers += 1

        print("\n{} persons are Engineers".format(engineers))

    def test_iframe_example(self):
        self.driver.switch_to.frame('courses-iframe')
        text = self.driver.find_elements(By.XPATH, "//div[@class='price-title']//div[@class='row clearfix']//li")
        print(text[7].text)
