import traceback
import urllib
import warnings
from pathlib import Path
import wget as wget
from selenium import webdriver
from bs4 import BeautifulSoup, element
import time
import re
import requests
import urllib3
from urllib.parse import urljoin

from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver import ActionChains
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from Mad_hq.Absolute_func import *
import mysql.connector
from multiprocessing.pool import ThreadPool
warnings.filterwarnings("ignore")



def fetching_categories():
    driver , display = runChromeOverServer()
    try:
        driver.get("https://us5.proxysite.one/")
        driver.maximize_window()
        time.sleep(3)
        driver.find_element_by_id("inputurl").clear()
        placing_url = driver.find_element_by_id("inputurl").send_keys("https://www.mad-hq.com/")
        clicking_button = driver.find_element_by_xpath("//*[@id='surfbtn']").send_keys(Keys.ENTER)
        time.sleep(7)
        driver.find_element_by_id("myproxy_show_hide_btn").click()
        print("Button Clicked")
        main_cate_ul = driver.find_element_by_css_selector(".navbar-nav").find_elements_by_css_selector(".menu-std")
        print(len(main_cate_ul))
        for iteration in main_cate_ul:
            main_cate_url = iteration.find_element_by_css_selector(".large-menu").get_attribute("href")
            main_cate_name = iteration.find_element_by_css_selector(".large-menu").text.strip()
            print(main_cate_name , main_cate_url)


            sub_cate_ul = iteration.find_element_by_css_selector(".dropdown-menu").find_element_by_css_selector(".col-lg-10").find_elements_by_css_selector(".dropdown")
            for iteration in sub_cate_ul:
                sub_cate_url = iteration.find_element_by_tag_name("ul").find_element_by_tag_name("a").get_attribute("href")
                try:
                    sub_cate_name = iteration.find_element_by_tag_name("ul").find_element_by_tag_name("a").text
                    print(sub_cate_name , sub_cate_url)
                except:
                    print(traceback)

        print("Button Clicked")


    except:
        traceback.print_exc()





if __name__ == '__main__':
    fetching_categories()