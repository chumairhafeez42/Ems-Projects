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
import mysql.connector
from multiprocessing.pool import ThreadPool



def runChromeOverServer():
    while True:
        try:
            # proo = AmazonProxies.objects.order_by('count')[0]
            # proxies = proo.proxy
            # proo.count += 1
            # proo.save()
            proxy= '172.254.124.231:3128'
            # proxy = '162.243.108.161:8080'
            from pyvirtualdisplay import Display
            # display = Display(visible=0, size=(1024, 768))
            # display.start()
            display = ''
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            # options.add_argument('--proxy-server=%s' % proxy)
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--shm-size=2g')
            options.add_argument('--no-sandbox')
            while True:
                try:
                    driver = webdriver.Chrome(executable_path='E:\Emsgroup\web_driver\chromedriver.exe')
                except:
                    driver = webdriver.Chrome(executable_path='E:\Emsgroup\web_driver\chromedriver.exe',
                        chrome_options=options)
                break
            return driver,display

        except Exception as e:
            print('driver while exception')
            print(e)
            pass



def fetching_categories():
    driver, display = runChromeOverServer()
    try:
        driver.execute_script("window.open('about:blank','tab1')")
        driver.switch_to.window("tab1")
        driver.get("https://www.sheetplastics.co.uk/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sub-nav__column")))
        main_nav = driver.find_elements_by_css_selector(".sub-nav__column")[0:3]
        p_id = 0
        for sublinks in main_nav:
             class_li = sublinks.find_elements_by_tag_name("li")
             for li in class_li:
                 a_ = li.find_element_by_tag_name("a")
                 main_cat_link = a_.get_attribute("href")
                 main_cat_name = a_.get_property("innerHTML")
                 print(main_cat_name , main_cat_link)

                 # try:
                 #     mydb = mysql.connector.connect(
                 #         host="localhost",
                 #         user="root",
                 #         passwd="",
                 #         database="plasticsheet"
                 #     )
                 #     mycursor = mydb.cursor()
                 #     sql = "INSERT INTO category (category_name,meta_title,meta_description,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
                 #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s)"
                 #     val = (
                 #         main_cat_name, main_cat_name, main_cat_name, "Yes", "Yes", "Yes", p_id,
                 #         main_cat_name.replace('-', '').replace('/', '').replace(' ','').strip(), "Yes")
                 #     mycursor.execute(sql, val)
                 #     mydb.commit()
                 #     print(mycursor.rowcount, "record inserted.")
                 #     mydb.close()
                 #
                 # except Exception as e:
                 #     print('Database query errror')
                 #     print(e)
                 try:
                     mydb = mysql.connector.connect(
                         host="localhost",
                         user="root",
                         passwd="",
                         database="plasticsheet"
                     )
                     mycursor = mydb.cursor()

                     sql = "SELECT category_id FROM category WHERE category_name ='%s'" % main_cat_name
                     mycursor.execute(sql)
                     myresult = mycursor.fetchall()
                     for x in myresult:
                         category_id = x[0]
                 except Exception as e:
                     print(e)
                     pass

                 try:
                     catelist = []
                     mydb = mysql.connector.connect(
                         host="localhost",
                         user="root",
                         passwd="",
                         database="plasticsheet"
                     )
                     mycursor = mydb.cursor()
                     sql = "SELECT category_id FROM products"
                     mycursor.execute(sql)
                     myresult = mycursor.fetchall()
                     for x in myresult:
                         cat_id = x[0]
                         catelist.append(cat_id)
                     if category_id in catelist:
                         pass
                         print("Already Exist in Database")
                     else:
                         extractproduct_urls(main_cat_link , category_id)
                 except:
                     pass

    except Exception as e:
        print(e)

    driver.quit()

def extractproduct_urls(main_cat_link , category_id):
    driver , display = runChromeOverServer()
    driver.execute_script("window.open('about:blank','tab2')")
    driver.switch_to.window("tab2")
    driver.get(main_cat_link)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-image")))
    product_url_div = driver.find_elements_by_css_selector(".product-image")
    product_urls_list =[]
    for anchor_tags in product_url_div:
        product_urls = anchor_tags.get_attribute("href")
        product_urls_list.append((product_urls , category_id))
    multipooling(product_urls_list)
    driver.quit()


def multipooling(product_url_list):
    print(len(product_url_list))
    chunksList = []
    for i in range(0, len(product_url_list), 1):
        chunk = product_url_list[i: i+1]
        chunksList.append(chunk)

        # print(chunksList)
    print(chunksList)
    # print(len(chunksList))
    # print(len(chunksList), " : ", chunksList)
    pool_size = 5
    pool = ThreadPool(pool_size)
    pool.map(products_data, chunksList)
    pool.close()
    pool.join()
    print('Done All Pool')

def products_data(chunksList):
    parent_url = 'https://www.sheetplastics.co.uk/'
    driver, display = runChromeOverServer()
    data_ = 10
    for url in chunksList:
        pro_url = url[0]
        cat_id = url[1]
        driver.execute_script("window.open('about:blank','tab" + str(data_) + "')")
        driver.switch_to.window("tab" + str(data_))
        driver.get(pro_url)
        try:
            product_title = driver.find_element_by_css_selector(".product-name").text
            print(product_title)
        except Exception as e:
            print(e)
        data_ += 1
    driver.quit()

def products():
    driver , display = runChromeOverServer()
    data_ = 1
    driver.execute_script("window.open('about:blank','tab" + str(data_) + "')")
    driver.switch_to.window("tab" + str(data_))
    driver.get("https://www.sheetplastics.co.uk/2mm-clear-acrylic-sheet-cut-to-size.html")
    try:
        product_title = driver.find_element_by_css_selector(".product-name").text
        print(product_title)
    except Exception as e:
        print(e)
    try:
        price_div = driver.find_element_by_css_selector(".regular-price")
        product_price = price_div.text
        print(product_price)
    except Exception as e:
        print(e)

    try:
        product_image_div = driver.find_element_by_css_selector(".product-image").find_element_by_tag_name("a")
        product_image = product_image_div.get_attribute("href")
        print(product_image)
    except Exception as e:
        print(e)
    try:
        desc_ = driver.find_element_by_css_selector(".tabbed-content__content.cf.tabbed-content__content--active").text
        print(desc_)
    except Exception as e:
        print(e)

    data_ += 1
    driver.quit()


if __name__ == '__main__':
    # fetching_categories()
    products()