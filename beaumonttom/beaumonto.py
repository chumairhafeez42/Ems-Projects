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
from beaumonttom.All_functions import *
import mysql.connector
from multiprocessing.pool import ThreadPool


def fetching_categories():
    driver , display = runChromeOverServer()
    try:
        data_ = 10
        driver.execute_script("window.open('about:blank','tab1')")
        driver.switch_to.window("tab1")
        driver.get("https://beaumonttm.co.uk/")
        driver.implicitly_wait(3)
        time.sleep(15)
        infinite_scrolling_PageDown(driver , 6)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-grid-layout")))
        infinite_scrolling_PageUp(driver , 5)
        p_id = 0
        cat_id = 0
        main_cate_div = driver.find_element_by_css_selector(".product-grid-layout").find_elements_by_css_selector(".et_pb_column")[1:]
        for iteration in main_cate_div:
            category_link = iteration.find_element_by_css_selector(".et_pb_blurb_container").find_element_by_tag_name("a").get_attribute("href")
            category_name = iteration.find_element_by_css_selector(".et_pb_blurb_container").find_element_by_tag_name("a").text
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".et_pb_blurb_content")))
            # try:
            #     category_image = iteration.find_element_by_css_selector(".et_pb_blurb_content").find_element_by_tag_name("img").get_attribute("src")
            #     cat_img_download_func(category_image, category_name)
            # except:
            #     print("Image not found")
            print(category_name , category_link)
            cat_id = cat_id + 1
            # try:
            #     val = (category_name, category_name, category_name, category_name.lower().replace('-', '').replace('/', '').replace(' ','').strip()+".jpg", "Yes", "Yes", "Yes", p_id,
            #         category_name.replace('-', '').replace('/', '').replace(' ','').strip(), "Yes")
            #     cat_data_insertion(val)
            # except Exception as e:
            #     print('Database query errror')
            #     print(e)

            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="beaumonttom"
                )
                mycursor = mydb.cursor()

                sql = "SELECT category_id FROM category WHERE category_name ='%s'" % category_name
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
                    product_links(driver , category_link , category_id , data_)
            except:
                pass
        driver.quit()
    except:
        pass

def product_links(driver , category_link , category_id , data_):
    try:
        driver.execute_script("window.open('about:blank','tab2')")
        driver.switch_to.window("tab2")
        driver.get(category_link)
        time.sleep(3)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".facetwp-template")))
        product_url_div = driver.find_element_by_css_selector(".facetwp-template")
        product_url_tag = product_url_div.find_elements_by_tag_name("li")
        product_urls_list = []
        for product_url_ahref in product_url_tag:
            product_url = product_url_ahref.find_element_by_tag_name('a').get_attribute("href")
            product_urls_list.append((category_id, product_url))
        print(product_urls_list)
        print(len(product_urls_list))
        multipooling(product_urls_list)
        data_ += 1
        driver.switch_to_window("tab1")
    except:
        pass


def pagination():
    driver , display = runChromeOverServer()
    driver.get("https://beaumonttm.co.uk/product-category/latest-products/")
    driver.implicitly_wait(10)
    time.sleep(60)
    infinite_scrolling_PageDown(driver , 7)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".facetwp-pager")))
    page_navigation = driver.find_element_by_css_selector(".facetwp-pager")  # pagination
    if page_navigation is not None:
        total_page = page_navigation.find_elements_by_tag_name('a')
        index_ = len(total_page) - 2
        total_page[index_].text.strip()
        totalpages = total_page[index_].text.strip()
        total_pages = int(totalpages.strip())
        current_url = driver.current_url
        for page_no in range(1, total_pages + 1):
            link = current_url + "?fwp_paged={0}".format(page_no)
            print(link)
            driver.get(link)
            time.sleep(5)
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".facetwp-template")))
            product_url_div = driver.find_element_by_css_selector(".facetwp-template")
            product_url_tag = product_url_div.find_elements_by_tag_name("li")
            product_urls_list = []
            category_id = 37
            for product_url_ahref in product_url_tag:
                product_url = product_url_ahref.find_element_by_tag_name('a').get_attribute("href")
                product_urls_list.append((category_id, product_url))
            print(product_urls_list)
            print(len(product_urls_list))
            multipooling(product_urls_list)
    driver.quit()

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
    driver , display = runChromeOverServer()
    try:
        data_ = 6
        for url in chunksList:
            pro_url = url[1]
            cat_id = url[0]
            try:
                driver.execute_script("window.open('about:blank','tab" + str(data_) + "')")
                driver.switch_to.window("tab" + str(data_))
                driver.get(pro_url)
                time.sleep(2)
                WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product_title")))
                try:
                    product_title = driver.find_element_by_css_selector(".product_title").text.strip()
                except:
                    pass

                try:
                    pdf = "https://beaumonttm.co.uk/wp-content/uploads/Beaumont-TM-Price-List-VI-3-3-2020.pdf"
                    description_div = driver.find_element_by_css_selector(".summary.entry-summary")
                    product_description = description_div.text.replace('Click here for ', '').replace('Additional information','').replace('\n','').strip()+ "\nFor More Details: "+ pdf
                except:
                    pass

                try:
                   product_image = driver.find_element_by_css_selector(".woocommerce-product-gallery__wrapper").find_element_by_tag_name('img').get_attribute('src')
                   prod_img_download_func(product_image , product_title)
                except:
                    pass
                price = int(4401525722500)

                try:
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        passwd="",
                        database="beaumonttom"
                    )
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO products (product_name,product_description,meta_title,meta_description,meta_keywords,status,category_id,feature_image,IsHome,IsFeature,IsSpecial,product_url,pro_price)" \
                          " VALUES (%s, %s,%s, %s, %s,%s, %s,%s,%s,%s,%s,%s,%s)"
                    val = (product_title, product_description, product_title,
                        product_title, product_title, "Yes", cat_id,
                        str(product_title).lower().replace(',', '').replace('-', '').replace(' ', '').replace('/','').replace('(', '').replace(')', '') + '.jpg',
                        'Yes', 'Yes', 'Yes', product_title, price)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print(mycursor.rowcount, "product inserted.")
                    mydb.close()
                except Exception as e:
                    print("Product not inserted")
                    print(e)

                try:
                    try:
                        mydb = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            passwd="",
                            database="beaumonttom"
                        )
                        mycursor = mydb.cursor()
                        sql = "SELECT product_id FROM products WHERE product_name = '%s'" % product_title
                        mycursor.execute(sql)
                        myresult = mycursor.fetchall()
                        for x in myresult:
                            product_id = x[0]
                        print('product_id is : ', product_id)
                        mydb.close()
                    except:
                        pass
                    z = 0
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".woocommerce-product-gallery__wrapper")))
                    product_image_div_ = driver.find_element_by_css_selector(".woocommerce-product-gallery__wrapper").find_elements_by_css_selector(".woocommerce-product-gallery__image")
                    if product_image_div_:
                        for image_div in product_image_div_:
                            product_images_ = image_div.find_element_by_tag_name('img').get_attribute('src')
                            multi_prod_img_download_func(product_images_, product_title, z)
                            try:
                                mydb = mysql.connector.connect(
                                    host="localhost",
                                    user="root",
                                    passwd="",
                                    database="beaumonttom"
                                )
                                mycursor = mydb.cursor()

                                sql = "INSERT INTO products_images (product_id,image_file)" \
                                      " VALUES (%s,%s)"
                                val = (product_id,
                                       str(product_title).lower().replace(',', '').replace('-', '').replace('/', '').replace(
                                           '@', '').replace(' ', '').replace('(', '').replace(')', '')+str(z)+'.jpg')
                                mycursor.execute(sql, val)
                                mydb.commit()
                                print(mycursor.rowcount, "product images inserted.")
                                mydb.close()
                            except Exception as e:
                                print(e)
                            z += 1
                    else:
                        pass
                except:
                    pass
            except:
                pass
            data_ += 1
    except:
        traceback.print_exc()

    driver.quit()




if __name__ == '__main__':
    fetching_categories()
    # pagination()