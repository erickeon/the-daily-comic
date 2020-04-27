import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options

class Scraper:
    def __init__(self):
        # set up headless browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'), \
            options=chrome_options)
    
    def get_comic(self):
        # get image link for top comic from reddit
        self.driver.get('https://www.reddit.com/r/comics/top/?t=day')
        sleep(2)
        img_link = self.driver.find_element_by_xpath("//img[@alt=\"Post image\"]").get_attribute('src')
        print(img_link)        
