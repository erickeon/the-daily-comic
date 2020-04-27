import os
import smtplib
from bs4 import BeautifulSoup
from email.message import EmailMessage
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
        self.img_link = self.driver.find_element_by_xpath("//img[@alt=\"Post image\"]").get_attribute('src')

    def send(self):
        # retrieve mail addresses
        EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
        EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
        SUBCRIBERS = [] # get subscriber emails from database
        # construct HTML mail
        mail_template = open("./mail_template.html", "r").read()
        soup = BeautifulSoup(mail_template, 'html.parser')
        div_tag = soup.find('div')
        img_tag = soup.new_tag('img', src=self.img_link)
        div_tag.append(img_tag)
        msg = EmailMessage()
        msg['Subject'] = 'Comic of the Day'
        msg['From'] = EMAIL_ADDRESS
        msg.add_alternative(str(soup),subtype='html')
        # send mail
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            for subscriber in SUBCRIBERS:
                print(subscriber)
                msg['To'] = subscriber
                smtp.send_message(msg)
                del msg['To']
        
s = Scraper()
s.get_comic()
s.send()
