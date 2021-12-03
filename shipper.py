import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import time
from selenium.webdriver.common.keys import Keys

#test

class orderInfo():
    def __init__(self, sku, price, quantity):
        self.sku = sku
        self.price = price
        self.quantity = quantity

def buylabels():

    os.system("taskkill /im chrome.exe /f")
    count = 1
    url = 'https://sellercentral.amazon.com/orders-v3/mfn/unshipped/?page=1'

    options = Options()
    options.headless = False
    options.add_experimental_option("detach", True)
    options.add_argument("--user-data-dir=C:/Users/sosa/AppData/Local/Google/Chrome/User Data")
    options.add_argument('--profile-directory=Profile 2')
    options.add_argument("--enable-javascript")

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get(url)
    browser.set_page_load_timeout(20)
    time.sleep(2)
    elements = browser.find_elements_by_xpath(f'//*[@id="orders-table"]/tbody/tr')
    print(len(elements))

    list_of_skus = []
    unique_skus = []
    def get_skus():
        for element in elements:
            sku = element.find_element_by_xpath(f'//*[@id="orders-table"]/tbody/tr[{elements.index(element)+1}]/td[5]/div/div/div[3]/div').get_attribute('innerHTML')[28:]
            list_of_skus.append(sku)
        print(list_of_skus)
        for i in list_of_skus:
            if i not in unique_skus:
                unique_skus.append(i)
        print(f'unique_skus: {unique_skus}')
        print('-------------------------------------')
        print('ORDERS TO SHIP:')
        for sku in unique_skus:
            print(f'{sku}: {list_of_skus.count(sku)} order(s)')

    def prep_labels():
        for sku in unique_skus:
            print(f'checking elements for {sku}')
            for element in elements:
                check_sku = element.find_element_by_xpath(f'//*[@id="orders-table"]/tbody/tr[{elements.index(element)+1}]/td[5]/div/div/div[3]/div').get_attribute('innerHTML')[28:]
                if check_sku == sku:
                    #click check box
                    checkbox = element.find_element_by_xpath(f'//*[@id="orders-table"]/tbody/tr[{elements.index(element)+1}]/td[1]/input')
                    checkbox.click()
            buy_shipping = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[3]/div[4]/div[2]/div[2]/div/div[1]/div/span[2]/span/span/a').send_keys(Keys.CONTROL, Keys.ENTER)
            for element in elements:
                check_sku = element.find_element_by_xpath(f'//*[@id="orders-table"]/tbody/tr[{elements.index(element)+1}]/td[5]/div/div/div[3]/div').get_attribute('innerHTML')[28:]
                if check_sku == sku:
                    #click check box
                    checkbox = element.find_element_by_xpath(f'//*[@id="orders-table"]/tbody/tr[{elements.index(element)+1}]/td[1]/input')
                    checkbox.click()
    get_skus()
    prep_labels()
    input("PRESS ENTER TO CLOSE")

buylabels()

#hello :)