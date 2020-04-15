import sys
import traceback
import urllib

import driver
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import requests
import urllib3
from urllib.parse import urljoin
from multiprocessing.pool import ThreadPool
from datetime import datetime
import mysql.connector
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

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
            exceptionMessage(e)
            pass

def exceptionMessage(e):
    print(traceback.format_exc())
    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

def infinite_scrolling_PageDown(driver, page_no):
    elem = driver.find_element_by_tag_name('body')
    while page_no:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        page_no -= 1

def infinite_scrolling_PageUp(driver, page_no):
    elem = driver.find_element_by_tag_name('body')
    while page_no:
        elem.send_keys(Keys.PAGE_UP)
        time.sleep(1)
        page_no -= 1

def cat_data_insertion(val):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="theworkplacedepot"
        )
        mycursor = mydb.cursor()

        sql = "INSERT INTO category (category_name,meta_title,meta_description,category_image,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
              " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s,%s)"
        mycursor.execute(sql, val)

        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        mydb.close()
    except Exception as e:
        print(e)

def page_scroller(driver , range_value):
    for i in range(0,range_value):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

def cat_img_download_func(img_url,img_name):
    urllib.request.urlretrieve(img_url, "E:\Emsgroup\cablematic_data\Images\category/" + img_name.replace(' ', '').replace('/', '').replace('_','')+".jpg")

def sub_cat_img_download_func(img_url,img_name):
    urllib.request.urlretrieve(img_url, "E:\Emsgroup\cablematic_data\Images\sub_category/" + img_name.replace(' ', '').replace('/', '').replace('_','')+".jpg")

def prod_img_download_func(img_url,img_name):
    urllib.request.urlretrieve(img_url, "E:\Emsgroup\cablematic_data\Images\product_images/" + img_name.replace(' ', '').replace('/', '').replace('_','')+".jpg")

def multi_prod_img_download_func(img_url,img_name,x):
    urllib.request.urlretrieve(img_url, "E:\Emsgroup\cablematic_data\Images\product_images/"+ img_name.replace(' ', '').replace('/', '').replace('_','')+str(x)+".jpg")


def runfirfoxOverServer():
    while True:
        try:
            # proo = AmazonProxies.objects.order_by('count')[0]
            # proxies = proo.proxy
            # proo.count += 1
            # proo.save()
            proxy= '159.89.138.73:8118'
            from pyvirtualdisplay import Display
            # display = Display(visible=0, size=(1024, 768))
            # display.start()
            # display = ''
            options = webdriver.FirefoxOptions()
            options.headless = True
            # options.add_argument('--proxy-server=%s' % proxy)
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--disable-web-security")
            options.add_argument('--shm-size=2g')
            options.add_argument('--no-sandbox')
            while True:
                try:
                    driver = webdriver.Firefox( executable_path=r'E:\Emsgroup\web_driver\geckodriver.exe',
                        firefox_options=options)
                except:
                    driver = webdriver.Firefox(executable_path=r'E:\Emsgroup\web_driver\geckodriver.exe',
                                               firefox_options=options)
                break
            return driver

        except Exception as e:
            print('driver while exception')
            exceptionMessage(e)
            pass

def firefox():
    options = Options()
    options.headless = True
    browser = webdriver.Firefox( executable_path=r'E:\Emsgroup\web_driver\geckodriver.exe')
    browser.get("https://google.com/")
    print ("Headless Firefox Initialized")
    browser.quit()


def db_insertion(sql , val):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="theworkplacedepot"
        )
        mycursor = mydb.cursor()

        mycursor.execute(sql, val)

        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        mydb.close()

    except Exception as e:
        print(e)


def cable_catinsertion(sql , val):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="theworkplacedepot"
        )
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        mydb.close()

    except Exception as e:
        print(e)


