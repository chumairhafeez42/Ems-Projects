import traceback
import urllib
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
from TheWorkPlaceDepot.absolute_workplace import *
import mysql.connector
from multiprocessing.pool import ThreadPool


def fetching_categories():
    driver , display= runChromeOverServer()
    data_ = 10
    driver.execute_script("window.open('about:blank','tab1')")
    driver.switch_to.window("tab1")
    driver.get("https://www.theworkplacedepot.co.uk/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "primary-nav")))
    main_cat_ul = driver.find_element_by_id("primary-nav").find_elements_by_css_selector(".section")
    p_id = 0
    cat_id = 0
    for atag in main_cat_ul:
        main_cat_links = atag.find_element_by_tag_name("a").get_attribute("href")
        main_cat_name = atag.find_element_by_tag_name("a").text
        print(main_cat_name , main_cat_links)
        # try:
        #     sql = "INSERT INTO category (category_name,meta_title,meta_description,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
        #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s)"
        #     val = (main_cat_name, main_cat_name, main_cat_name, "Yes", "Yes", "Yes", p_id,
        #         main_cat_name.replace('-', '').replace('/', '').replace(' ','').strip(), "Yes")
        #     cable_catinsertion(sql, val)
        # except Exception as e:
        #     print('Database query errror')
        #     print(e)
        Sub_cat_ul = atag.find_element_by_css_selector(".dropdown-menu").find_elements_by_tag_name("a")
        cat_id = cat_id + 1
        p1_id = cat_id
        for ancho_tag in Sub_cat_ul:
            sub_cat_name = ancho_tag.get_attribute('innerHTML')
            sub_cat_url = ancho_tag.get_attribute("href")
            print(sub_cat_name , sub_cat_url)
            # try:
            #     sql = "INSERT INTO category (category_name,meta_title,meta_description,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
            #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s)"
            #     val = (sub_cat_name, sub_cat_name, sub_cat_name, "Yes", "Yes", "Yes", p1_id,
            #         sub_cat_name.replace('-', '').replace('/', '').replace(' ','').strip(), "Yes")
            #     cable_catinsertion(sql, val)
            # except Exception as e:
            #     print('Database query errror')
            #     print(e)
            cat_id = cat_id + 1
            driver.switch_to_window("tab1")
            driver.execute_script("window.open('about:blank','tab2')")
            driver.switch_to.window("tab2")
            product_url_list = []
            driver.get(sub_cat_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "category-tiles")))
            product_url_div = driver.find_element_by_id("category-tiles").find_elements_by_css_selector(".tile-products")
            for link in product_url_div:
                product_url = link.find_element_by_tag_name("a").get_attribute("href")
                print("product_url:", product_url)
                product_url_list.append(product_url)
            data_ += 1

    driver.quit()



if __name__ == '__main__':
    fetching_categories()










