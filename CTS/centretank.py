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
from CTS.All_functions import *
import mysql.connector
from multiprocessing.pool import ThreadPool
warnings.filterwarnings("ignore")



def fetching_categories():
    driver , display  = runChromeOverServer()
    try:
        driver.execute_script("window.open('about:blank','tab')")
        driver.switch_to.window("tab")
        driver.get("https://www.centretank.com/products")
        time.sleep(2)
        data_ = 10
        p_id = 0
        cat_id = 0
        main_cat_div = driver.find_element_by_css_selector(".product-category-contain").find_elements_by_css_selector(".product-category-grid")
        for iteration in main_cat_div:
            main_cat_links = iteration.find_element_by_css_selector(".product-category-grid-image").find_element_by_tag_name("a").get_attribute("href")
            main_cat_name = iteration.find_element_by_css_selector(".product-category-grid-image").find_element_by_tag_name("a").get_attribute("title")
            main_cat_image = iteration.find_element_by_css_selector(".product-category-grid-image").find_element_by_tag_name("a").find_element_by_tag_name("img").get_attribute("src")
            cat_img_download_func(main_cat_image, main_cat_name)
            print(p_id , main_cat_name , main_cat_links , main_cat_image)
            try:
                val = (main_cat_name, main_cat_name, main_cat_name, main_cat_name.lower().replace('-', '').replace('/', '').replace(' ','').replace('&','').strip()+".jpg", "Yes", "Yes", "Yes", p_id,
                    main_cat_name.replace('-', '').replace('/', '').replace(' ','').strip(), "Yes")
                cat_data_insertion(val)
            except Exception as e:
                print('Database query errror')
                print(e)

            driver.execute_script("window.open('about:blank','tab1')")
            driver.switch_to.window("tab1")
            driver.get(main_cat_links)
            time.sleep(2)
            infinite_scrolling_PageDown(driver, 1)
            try:
                sub_cat_div = driver.find_elements_by_css_selector(".product-category-shortcut-link")
                if sub_cat_div:
                    cat_id = cat_id + 1
                    p1_id = cat_id
                    for atag in sub_cat_div:
                        sub_cat_links = atag.get_attribute("href")
                        sub_tag_img = atag.find_element_by_tag_name("img").get_attribute("src")
                        sub_cat_name = atag.find_element_by_tag_name("span").text
                        sub_cat_img_download_func(sub_tag_img, sub_cat_name)
                        print("1st loops:", p1_id , sub_cat_name , sub_cat_links , sub_tag_img)
                        try:
                            val = (sub_cat_name, sub_cat_name, sub_cat_name,sub_cat_name.lower().replace('-', '').replace('/', '').replace(' ','').replace('&','').strip() + ".jpg",
                                   "Yes", "Yes", "Yes", p1_id, sub_cat_name.replace('-', '').replace('/', '').replace(' ', '').strip(), "Yes")
                            cat_data_insertion(val)
                        except Exception as e:
                            print('Database query errror')
                            print(e)
                        ##### extract_categories(driver , sub_cat_links , data_ , cat_id)
                        try:
                            driver.execute_script("window.open('about:blank','tab2')")
                            driver.switch_to.window("tab2")
                            driver.get(sub_cat_links)
                            time.sleep(2)
                            sub_sub_cat_div = driver.find_elements_by_css_selector(".product-category-shortcut-link")
                            if sub_sub_cat_div:
                                cat_id = cat_id + 1
                                p2_id = cat_id
                                for atag in sub_sub_cat_div:
                                    sub_sub_cat_links = atag.get_attribute("href")
                                    sub_sub_tag_img = atag.find_element_by_tag_name("img").get_attribute("src")
                                    sub_sub_cat_name = atag.find_element_by_tag_name("span").text
                                    sub_cat_img_download_func(main_cat_image, sub_sub_cat_name)
                                    print("2nd loops:", p2_id, sub_sub_cat_name, sub_sub_cat_links, sub_sub_tag_img)
                                    try:
                                        val = (sub_sub_cat_name, sub_sub_cat_name, sub_sub_cat_name,sub_sub_cat_name.lower().replace('-', '').replace('/', '').replace(' ','').replace('&','').strip() + ".jpg",
                                               "Yes", "Yes", "Yes", p2_id, sub_sub_cat_name.replace('-', '').replace('/', '').replace(' ', '').strip(), "Yes")
                                        cat_data_insertion(val)
                                    except Exception as e:
                                        print('Database query errror')
                                        print(e)
                                    cat_id = cat_id + 1
                                    final_cat_links = sub_sub_cat_links
                                    final_cat_name = sub_sub_cat_name
                                    # pagination(driver , final_cat_links , final_cat_name)
                                data_ += 1
                                driver.switch_to_window("tab1")
                            else:
                                print("Else2..........................")
                                cat_id = cat_id + 1
                                final_cat_links = sub_cat_links
                                final_cat_name = sub_cat_name
                                # pagination(driver , final_cat_links , final_cat_name)
                            data_ += 1
                            driver.switch_to_window("tab1")
                        except:
                            pass
                    data_ += 1
                    driver.switch_to_window("tab")
                else:
                    print("Else1.................")
                    final_cat_links = main_cat_links
                    final_cat_name = main_cat_name
                    # pagination(driver , final_cat_links , final_cat_name)
                data_ += 1
                driver.switch_to_window("tab")

            except Exception as e:
                pass
    except:
        pass
    driver.quit()

def pagination(driver , final_cat_links , final_cat_name):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="beaumonttom"
        )
        mycursor = mydb.cursor()

        sql = "SELECT category_id FROM category WHERE category_name ='%s'" % final_cat_name
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
            database="beaumonttom"
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
            data_ = 5
            product_url_list = []
            try:
                driver.execute_script("window.open('about:blank','tab3')")
                driver.switch_to.window("tab3")
                driver.get(final_cat_links)
                time.sleep(1)
                infinite_scrolling_PageDown(driver, 2)
                product_url_div = driver.find_element_by_css_selector(
                    ".product-grid-contain").find_elements_by_css_selector(".product-grid-image")
                for atag in product_url_div:
                    product_links = atag.find_element_by_tag_name("a").get_attribute("href")
                    product_url_list.append(product_links)
                try:
                    Page_navigation = driver.find_element_by_css_selector(
                        ".product-pagination").find_elements_by_tag_name("li")[1::]
                    if Page_navigation:
                        print("Entered in Pagination")
                        for iteration in Page_navigation:
                            current_url = iteration.find_element_by_tag_name("a").get_attribute("href")

                            driver.get(current_url)
                            time.sleep(2)
                            product_url_div = driver.find_element_by_css_selector(
                                ".product-grid-contain").find_elements_by_css_selector(".product-grid-image")
                            for atag in product_url_div:
                                product_links = atag.find_element_by_tag_name("a").get_attribute("href")
                                product_url_list.append(product_links)

                        data_ += 1
                        driver.switch_to_window("tab2")
                    else:
                        print("No More Pagination")

                except:
                    pass
                print(len(product_url_list), product_url_list)
                # multipooling(product_url_list)
                data_ += 1
                driver.switch_to_window("tab2")
            except:
                pass
    except:
        pass


def multipooling(product_url_list):
    print(len(product_url_list))
    chunksList = []
    for i in range(0, len(product_url_list), 6):
        chunk = product_url_list[i: i+6]
        chunksList.append(chunk)
        # print(chunksList)
    print(chunksList)
    # print(len(chunksList))
    # print(len(chunksList), " : ", chunksList)
    pool_size = 3
    pool = ThreadPool(pool_size)
    pool.map(Product_data, chunksList)
    pool.close()
    pool.join()
    print('Done All Pool')

def Product_data(chunksList):
    driver, display = runChromeOverServer()
    try:
        data_ = 12
        for url in chunksList:
            pro_url = url
            # cat_id = url[0]
            try:
                driver.execute_script("window.open('about:blank','tab" + str(data_) + "')")
                driver.switch_to.window("tab" + str(data_))
                driver.get(pro_url)
                time.sleep(2)
                try:
                    product_title = driver.find_element_by_css_selector(".product-titles").text.replace("\n", " ").strip()
                    print(product_title)
                except:
                    pass


                try:
                    product_price = driver.find_element_by_css_selector(".price-container").find_element_by_css_selector(".p-price").text.replace("£",'').strip()
                    print(product_price)
                except:
                    pass

                try:
                    product_description_div = driver.find_element_by_css_selector(".product-cat-desc")
                    product_description = product_description_div.text.replace("\n", "").strip()
                    print(product_description)
                except:
                    pass

                try:
                   product_images = driver.find_element_by_css_selector(".product-images").find_element_by_css_selector(".product-image-main").find_element_by_tag_name("img").get_attribute("src")
                   print(product_images)
                except:
                    pass

                try:
                    product_variation_divs = driver.find_element_by_css_selector(".product-table").find_elements_by_tag_name("tr")[1::]
                    for iteration in product_variation_divs:
                        product_code = iteration.find_element_by_css_selector(".p-t-code").text.strip()
                        product_model = iteration.find_element_by_css_selector(".p-t-model").text.strip()
                        product_price_ = iteration.find_element_by_css_selector(".p-t-price").text.strip()
                        print(product_code , product_model , product_price_)
                except:
                    traceback.print_exc()

                try:
                    infinite_scrolling_PageDown(driver , 3)
                    Acessories = driver.find_element_by_xpath("/html/body/div[6]/div[2]/div[1]/div[5]/ul/li[2]/a").click()
                    time.sleep(1)
                    product_variation_divs = driver.find_element_by_css_selector(".product-table-accessories").find_elements_by_tag_name("tr")[1::]
                    for iteration in product_variation_divs:
                        product_code = iteration.find_element_by_css_selector(".p-t-code").text.strip()
                        product_model = iteration.find_element_by_css_selector(".p-t-accessory").text.replace("\n"," ").strip()
                        product_price_ = iteration.find_element_by_css_selector(".p-t-price").text.strip()
                        print(product_code, product_model, product_price_)
                except:
                   traceback.print_exc()
            except:
                pass

            data_ += 1
    except:
        traceback.print_exc()

def extract_categories(driver , sub_cat_links , data_ , cat_id):
    try:
        driver.execute_script("window.open('about:blank','tab2')")
        driver.switch_to.window("tab2")
        driver.get(sub_cat_links)
        time.sleep(2)
        sub_sub_cat_div = driver.find_elements_by_css_selector(".product-category-shortcut-link")
        if sub_sub_cat_div:
            cat_id = cat_id + 1
            p2_id = cat_id
            for atag in sub_sub_cat_div:
                sub_sub_cat_links = atag.get_attribute("href")
                sub_sub_tag_img = atag.find_element_by_tag_name("img").get_attribute("src")
                print("2nd loops:", p2_id ,  sub_sub_cat_links, sub_sub_tag_img)
                cat_id = cat_id + 1
                final_cat_links = sub_sub_cat_links
                # pagination(driver, final_cat_links)
            data_ += 1
            driver.switch_to_window("tab1")
        else:
            print("Else2..........................")
            final_cat_links = sub_cat_links
            # pagination(driver, final_cat_links)
        data_ += 1
        driver.switch_to_window("tab1")
    except:
        pass





if __name__ == '__main__':
    fetching_categories()