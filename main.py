import re
import sys
import time
import logging
import subprocess

from stem.util import system, term
from stem import process as tor_process
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from TorInit import TorInit


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

### example code
class Crawl(TorInit):

  def __init__(self, socks_port, url):
    '''

    init tor socks port and init chrome 

    socks port default = 9050

    '''
    self.TorInit = TorInit(socks_port=socks_port)
    self.TorInit.startTorProxy()

    #init chrome options -> tor proxy 
    proxy = "socks5://127.0.0.1:{}".format(socks_port)
    opts = Options()
    opts.add_argument('--proxy-server={}'.format(proxy)) 
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'

    opts.add_argument("user-agent={}".format(USER_AGENT))    

    self.browser = webdriver.Chrome(executable_path = "./chrome/chromedriver", chrome_options=opts)
    self.browser.implicitly_wait(10)
    self.url = url

  def login(self):
    '''

    browse example 
    
    some onion site need to input account, password and recaptcha.
    
    you can use selenium chrome login and get cookies after you login.

    this is a simple example 

    '''
    self.browser.get(self.url)
    #after login
    self.browser.find_element_by_id("id_username").send_keys("testestestor")
    self.browser.find_element_by_id("id_password").send_keys("testestestor")
    captcha = self.browser.find_element_by_id("id_captchainput")
    logging.info("Input captcha : ")
    captcha.send_keys(input())
    captcha.send_keys(Keys.ENTER)

    '''
    if you do not use request, you can use selenium to do crawl job
    

    ### parse you want
    
    '''

    # get your cookies and use request to do crawl ~ 

    return self.browser.get_cookies()

  def parse(self):
    #do your crawl job
    pass

if __name__ == '__main__':

  crawler = Crawl(socks_port=9050, url="http://greenroxwc5po3ab.onion/")
  cookies = crawler.login()
  logging.info(cookies)
  
