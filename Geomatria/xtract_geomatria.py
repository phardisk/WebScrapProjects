from selenium import webdriver
import ssl
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

lst_word=['Cameron','Florence','lion','Camelot','Ufc', 'married', 'the scream','life path', 'I see fire']
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode =ssl.CERT_NONE
url='https://www.gematrix.org'
#driver = webdriver.Chrome('selenium/chromedriver.exe')
driver = webdriver.Chrome()
driver.get(url)
for suffixe in lst_word:
    print(f"Processing for {suffixe}....")
    time.sleep(2)
    driver.find_element_by_xpath("//input[@type='search']").clear()
    driver.find_element_by_xpath("//input[@type='search']").send_keys(suffixe)
    submit = driver.find_element_by_xpath("//input[@type='submit']")
    submit.click()
    time.sleep(10)
    print("For word or group of words:", suffixe)
    result = driver.find_elements_by_tag_name('strong')
    print("The Jewish gematria value is", result[0].text)
    print("The English gematria value is", result[1].text)
    print("The Simple gematria value is", result[2].text)











