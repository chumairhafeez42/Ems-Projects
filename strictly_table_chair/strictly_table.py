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

from selenium.webdriver import ActionChains
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from strictly_table_chair.absolute_tablechair import *
import mysql.connector
from multiprocessing.pool import ThreadPool
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime


def fetching_cateogry():
    try:
        # driver = webdriver.Chrome(executable_path=r"E:\Emsgroup\web_driver\chromedriver.exe")
        driver = runfirfoxOverServer()
        driver.execute_script("window.open('about:blank','tab1')")
        driver.switch_to.window("tab1")
        driver.get("https://www.strictlytablesandchairs.co.uk/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".menu-wrapper")))
        main_nav_class_ = driver.find_element_by_css_selector(".menu-wrapper")
        main_cate_li = main_nav_class_.find_elements_by_tag_name("li.menu-full-width")
        p_id = 0
        cat_id = 0
        data_ = 10
        for li in main_cate_li:
            a_ = li.find_element_by_tag_name('a')
            main_cat_links = a_.get_attribute('href')
            main_cat_name = a_.get_property('innerHTML').strip()
            print(p_id , main_cat_name , main_cat_links)
            # try:
            #     sql = "INSERT INTO category (category_name,meta_title,meta_description,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
            #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s)"
            #     val = (
            #         main_cat_name, main_cat_name, main_cat_name, "Yes", "Yes", "Yes", p_id,
            #         main_cat_name.replace('-', '').replace('/', '').replace(' ','').strip(), "Yes")
            #     cat_data_insertion(sql, val)
            # except Exception as e:
            #     print('Database query errror')
            #     print(e)
            Sub_category(driver,p_id, cat_id , main_cat_links , data_)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.menu-parent-item")))
        main_cate_li = main_nav_class_.find_elements_by_css_selector("li.menu-parent-item")
        for li in main_cate_li:
            a_ = li.find_element_by_tag_name("a")
            main_cat_links = a_.get_attribute("href")
            main_cat_name = a_.get_property("innerHTML").strip()
            # try:
            #     sql = "INSERT INTO category (category_name,meta_title,meta_description,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
            #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s)"
            #     val = (
            #         main_cat_name, main_cat_name, main_cat_name, "Yes", "Yes", "Yes", p_id,
            #         main_cat_name.replace('-', '').replace('/', '').replace(' ', '').strip(), "Yes")
            #     cat_data_insertion(sql, val)
            # except Exception as e:
            #     print('Database query errror')
            #     print(e)
            Sub_category(driver,p_id, cat_id , main_cat_links , data_)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[1]/div[3]/div/div/div/div/ul/li[6]/a")))
        a_tag = driver.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div[3]/div/div/div/div/ul/li[6]/a")
        for a_ in a_tag:
            main_cat_links = a_.get_attribute('href')
            main_cat_name = a_.get_property("innerHTML").strip()
            # try:
            #     sql = "INSERT INTO category (category_name,meta_title,meta_description,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
            #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s)"
            #     val = (main_cat_name, main_cat_name, main_cat_name, "Yes", "Yes", "Yes", p_id,
            #         main_cat_name.replace('-', '').replace('/', '').replace(' ', '').strip(), "Yes")
            #     cat_data_insertion(sql, val)
            # except Exception as e:
            #     print('Database query errror')
            #     print(e)
            Sub_category(driver,p_id,cat_id , main_cat_links , data_)

    except:
        traceback.print_exc()
    driver.quit()


def Sub_category(driver ,p_id, cat_id , main_cat_links, data_):

    # <--------------------------------Danger Zone------------------------------------>

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="tablechair"
        )
        mycursor = mydb.cursor()
        sql = "SELECT category_id FROM category"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            cat_id = x[0]
        print('category_id is : ', cat_id)
        mydb.close()
    except:
        pass

    # <--------------------------------Danger Zone------------------------------------>
    try:
        driver.execute_script("window.open('about:blank','tab2')")
        driver.switch_to.window("tab2")
        driver.get(main_cat_links)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".apptrian-subcategories")))
        sub_cat_div = driver.find_elements_by_css_selector(".apptrian-subcategories")
        for sub_cat_li in sub_cat_div:
            sub_cat_a_tag = sub_cat_li.find_elements_by_tag_name("a")
            p1_id = cat_id
            for a_tag in sub_cat_a_tag:
                sub_cat_links = a_tag.get_attribute('href')
                sub_cat_names = a_tag.find_element_by_tag_name("span").text.strip()
                sub_cat_images = a_tag.find_element_by_tag_name("img").get_attribute('src')
                sub_cat_img_download_func(sub_cat_images , sub_cat_names)
                print(p1_id, cat_id, sub_cat_links , sub_cat_names)
                # try:
                #     sql = "INSERT INTO category (category_name,meta_title,meta_description,category_image,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
                #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s,%s)"
                #     val = (
                #         sub_cat_names, sub_cat_names, sub_cat_names,sub_cat_names.lower().replace('/','').replace('-','').replace(',','').replace('@','')+'.jpg', "Yes", "Yes", "Yes", p1_id,
                #         sub_cat_names.replace('-', '').replace('/', '').replace(' ', '').strip(), "Yes")
                #     cat_data_insertion(sql, val)
                # except Exception as e:
                #     print('Database query errror')
                #     print(e)
                cat_id = cat_id + 1
                try:
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        passwd="",
                        database="tablechair"
                    )
                    mycursor = mydb.cursor()

                    sql = "SELECT category_id FROM category WHERE category_name ='%s'" % sub_cat_names
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
                        database="tablechair"
                    )
                    mycursor = mydb.cursor()
                    sql = "SELECT category_id FROM products"
                    mycursor.execute(sql)
                    myresult = mycursor.fetchall()
                    for x in myresult:
                        catid = x[0]
                        catelist.append(catid)
                    print(catelist)
                    if category_id in catelist:
                        Fetching_Producturls(driver, sub_cat_links, category_id, data_)
                        print("Already Exist in Database")
                    else:
                        Fetching_Producturls(driver, sub_cat_links, category_id,data_)
                except:
                    pass
                data_ += 1
            driver.switch_to_window("tab1")

    except:
        traceback.print_exc()


def Fetching_Producturls(driver , sub_cat_links, category_id, data_):
    try:
        product_urls_list = []
        driver.execute_script("window.open('about:blank','tab3')")
        driver.switch_to.window("tab3")
        driver.get(sub_cat_links)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".limiter")))
        try:
            driver.find_element_by_xpath("/html/body/div[3]/div/div[5]/div/div[1]/div[1]/div[4]/div[2]/div/div/div[3]/select").click()
            driver.find_element_by_xpath("/html/body/div[3]/div/div[5]/div/div[1]/div[1]/div[4]/div[1]/div/div[3]/select/option[2]").click()
            print("Selected")
        except:
            pass
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".products-grid")))
        page_scroller(driver, 5)
        product_url_div = driver.find_elements_by_css_selector('.item-area')
        for atag in product_url_div:
            product_url_atag = atag.find_elements_by_css_selector(".product-image")
            for product_link_tag in product_url_atag:
                product_link = product_link_tag.get_attribute('href')
                product_urls_list.append((category_id, product_link))
        print(product_urls_list)
        print(len(product_urls_list))
        multipooling(product_urls_list)
        driver.switch_to_window('tab2')




    except:
        traceback.print_exc()


def multipooling(product_url_list):
    print(len(product_url_list))
    chunksList = []
    for i in range(0, len(product_url_list), 5):
        chunk = product_url_list[i: i+5]
        chunksList.append(chunk)

        # print(chunksList)
    print(chunksList)
    # print(len(chunksList))
    # print(len(chunksList), " : ", chunksList)
    pool_size = 4
    pool = ThreadPool(pool_size)
    pool.map(varriations, chunksList)
    pool.close()
    pool.join()
    print('Done All Pool')


def Product_Data(chunksList):
    driver = runfirfoxOverServer()
    # driver = webdriver.Chrome(executable_path=r"E:\Emsgroup\web_driver\chromedriver.exe")
    data_ = 5
    for url in chunksList:
        pro_url = url[1]
        cat_id = url[0]
        try:
            driver.execute_script("window.open('about:blank','tab" + str(data_) + "')")
            driver.switch_to.window("tab" + str(data_))
            driver.get(pro_url)
            print(pro_url)
            # driver.execute_script("window.open('about:blank','tab1')")
            # driver.switch_to.window("tab1")

            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-view ")))
            try:
                product_title_div = driver.find_element_by_css_selector(".product-name")
                product_title = product_title_div.find_element_by_tag_name('h1').text.strip()
                print(product_title)
            except Exception as e:
                print(e)

            try:
                price_div = driver.find_elements_by_css_selector(".price-excluding-tax")
                for price_ in price_div:
                    price = price_.text.replace('£', '').strip()
                    print(price)
            except Exception as e:
                print(e)

            try:
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".short-description")))
                product_description_div = driver.find_elements_by_css_selector(".short-description")
                for product_description_ in product_description_div:
                    product_description_tag = product_description_.find_element_by_tag_name('p')
                    TechSpecs_ = product_description_tag.text.replace("• ", '').strip()
                    print(TechSpecs_)
            except Exception as e:
                print(e)

            try:
                product_description_details = driver.find_elements_by_id('tab_description_tabbed_contents')
                for pro_desc in product_description_details:
                    techspecs = pro_desc.text
                    product_description_ = techspecs.split('\n')[0]
                    print(product_description_)
                    if TechSpecs_:
                        product_description = (TechSpecs_ + product_description_)
                    else:
                        pass
            except:
                pass

            try:
                fabric_color_div = driver.find_element_by_xpath(
                    "//*[@id='product_addtocart_form']/div[2]/div[2]/div[2]/div/p[3]/strong[1]/a")
                if fabric_color_div:
                    fabric_color = fabric_color_div.get_attribute("href")
                    product_description = (product_description + fabric_color)
                else:
                    pass
            except:
                pass

            try:
                pdf_link_div = driver.find_element_by_xpath(
                    "//*[@id='product_addtocart_form']/div[2]/div[2]/div[2]/div/p[2]/a")
                if pdf_link_div is not None:
                    pdf_link = pdf_link_div.get_attribute("href")
                    print(pdf_link)
                    product_description = (product_description + pdf_link)
                    print(product_description)
                else:
                    pdf_link_div = driver.find_element_by_xpath(
                        "//*[@id='product_addtocart_form']/div[2]/div[2]/div[2]/div/p[2]/strong[1]/a")
                    if pdf_link_div:
                        pdf_link = pdf_link_div.get_attribute("href")
                        print(pdf_link)
                        product_description = (product_description + pdf_link)
                        print(product_description)
                    else:
                        pass
            except:
                pass

            try:
                images_div = driver.find_element_by_css_selector('.etalage_thumb_image')
                product_image = images_div.get_attribute("src")
                prod_img_download_func(product_image, product_title)
                print(product_image)
            except Exception as e:
                print(e)
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="tablechair"
                )

                mycursor = mydb.cursor()

                sql = "INSERT INTO products (product_name,product_description,meta_title,meta_description,meta_keywords,status,category_id,feature_image,IsHome,IsFeature,IsSpecial,product_url,pro_price)" \
                      " VALUES (%s, %s,%s, %s, %s,%s, %s,%s,%s,%s,%s,%s,%s)"
                val = (
                    product_title, product_description, product_title,
                    product_title, product_title, "Yes", cat_id,
                    str(product_title).lower().replace(',', '').replace('-', '').replace(' ', '').replace('/',
                                                                                                          '').replace(
                        '(', '').replace(')', '') + '.jpg',
                    'Yes', 'Yes', 'Yes', product_title, price)
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "product inserted.")
                mydb.close()
            except Exception as e:
                print("Product not inserted")
                print(e)

            try:
                images_div = driver.find_elements_by_css_selector(".etalage_thumb_image")
                if images_div is not None:
                    try:
                        mydb = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            passwd="",
                            database="tablechair"
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
                    for image_tags in images_div:
                        product_images = image_tags.get_attribute("src")
                        multi_prod_img_download_func(product_images, product_title, z)
                        try:
                            mydb = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                passwd="",
                                database="tablechair"
                            )
                            mycursor = mydb.cursor()

                            sql = "INSERT INTO products_images (product_id,image_file)" \
                                  " VALUES (%s,%s)"
                            val = (product_id,
                                   str(product_title).lower().replace(',', '').replace('-', '').replace('/','').replace(
                                       '@', '').replace(' ', '').replace('(', '').replace(')', '')+ '.jpg')
                            mycursor.execute(sql, val)
                            mydb.commit()
                            print(mycursor.rowcount, "product images inserted.")
                            mydb.close()
                        except Exception as e:
                            print(e)
                        z += 1
                else:
                    pass
            except Exception as e:
                print(e)
        except:
            traceback.print_exc()
        data_ +=1

    driver.quit()


def varriations(chunksList):
    driver = runfirfoxOverServer()
    # driver = webdriver.Chrome(executable_path=r"E:\Emsgroup\web_driver\chromedriver.exe")
    try:
        size_id = 0
        data_ = 5
        for url in chunksList:
            pro_url = url[1]
            cat_id = url[0]
            try:
                driver.execute_script("window.open('about:blank','tab" + str(data_) + "')")
                driver.switch_to.window("tab" + str(data_))
                driver.get(pro_url)
                print(pro_url)
                # driver.execute_script("window.open('about:blank','tab1')")
                # driver.switch_to.window("tab1")
                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-view ")))
                try:
                    product_title_div = driver.find_element_by_css_selector(".product-name")
                    product_title = product_title_div.find_element_by_tag_name('h1').text.strip()
                    print(product_title)
                except Exception as e:
                    print(e)

                try:
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        passwd="",
                        database="tablechair"
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
                size_id = size_id
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-custom-option")))
                    color_variation_div = driver.find_element_by_css_selector(".product-custom-option")
                    if color_variation_div is not None:
                        options = color_variation_div.find_elements_by_tag_name("option")[1:]
                        time.sleep(2)
                        for option in options:
                            option.click()
                            print("clicked")
                            fabric_color = option.text.strip()
                            price_div = driver.find_element_by_css_selector(".price-excluding-tax")
                            price = price_div.text.replace('£', '').strip()
                            size_id += 1
                            if price is not None:
                                fabric_color1 = fabric_color + "-" + price
                                print(fabric_color1)
                                try:
                                    mydb = mysql.connector.connect(
                                        host="localhost",
                                        user="root",
                                        passwd="",
                                        database="tablechair"
                                    )
                                    mycursor = mydb.cursor()

                                    sql = "INSERT INTO products_size(size_id,product_id, price,size)" \
                                          " VALUES (%s,%s,%s,%s)"
                                    val = (size_id, product_id, price, fabric_color1)
                                    mycursor.execute(sql, val)
                                    mydb.commit()
                                    print(mycursor.rowcount, "size_product inserted.")
                                    mydb.close()
                                except Exception as e:
                                    print(e)
                                    pass
                            else:
                                pass
                            try:
                                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ox-picker")))
                                variation_div = driver.find_elements_by_css_selector('.ox-picker')
                                if variation_div is not None:
                                    time.sleep(1)
                                    for variation_tags in variation_div:
                                        time.sleep(2)
                                        options = variation_tags.find_elements_by_tag_name('img')
                                        for option in options:
                                            time.sleep(1)
                                            option.click()
                                            image_tags = option.get_attribute('src')
                                            pro_images = image_tags.split('/')[-1]
                                            fabric_color_ = pro_images.replace('.png', '').replace('.jpeg', '').replace('.jpg', '')
                                            price_div = driver.find_element_by_css_selector(".price-excluding-tax")
                                            price = price_div.text.replace('£', '').strip()
                                            size_id += 1
                                            if price is not None:
                                                fabric_color2 = fabric_color_ + "-" + price
                                                print(fabric_color2)
                                                try:
                                                    mydb = mysql.connector.connect(
                                                        host="localhost",
                                                        user="root",
                                                        passwd="",
                                                        database="tablechair"
                                                    )
                                                    mycursor = mydb.cursor()

                                                    sql = "INSERT INTO products_size(size_id,product_id, price,size)" \
                                                          " VALUES (%s,%s,%s,%s)"
                                                    val = (size_id, product_id, price, fabric_color2)
                                                    mycursor.execute(sql, val)
                                                    mydb.commit()
                                                    print(mycursor.rowcount, "size_product inserted.")
                                                    mydb.close()
                                                except Exception as e:
                                                    print(e)
                                                    pass
                                            else:
                                                pass
                                        time.sleep(2)
                                else:
                                    pass
                            except:
                                pass
                    else:
                        pass
                except:
                    pass

                try:
                    print("Entered in Color Varriations")
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ox-picker")))
                    variation_div = driver.find_elements_by_css_selector('.ox-picker')
                    if variation_div is not None:
                        time.sleep(1)
                        for variation_tags in variation_div:
                            time.sleep(2)
                            options = variation_tags.find_elements_by_tag_name('img')
                            for option in options:
                                time.sleep(1)
                                option.click()
                                image_tags = option.get_attribute('src')
                                pro_images = image_tags.split('/')[-1]
                                fabric_color_ = pro_images.replace('.png', '').replace('.jpeg', '').replace('.jpg', '')
                                price_div = driver.find_element_by_css_selector(".price-excluding-tax")
                                price = price_div.text.replace('£', '').strip()
                                size_id += 1
                                if price is not None:
                                    fabric_color3 = fabric_color_ + "-" + price
                                    print(fabric_color3)
                                    try:
                                        mydb = mysql.connector.connect(
                                            host="localhost",
                                            user="root",
                                            passwd="",
                                            database="tablechair"
                                        )
                                        mycursor = mydb.cursor()

                                        sql = "INSERT INTO products_size(size_id,product_id, price,size)" \
                                              " VALUES (%s,%s,%s,%s)"
                                        val = (size_id, product_id, price, fabric_color3)
                                        mycursor.execute(sql, val)
                                        mydb.commit()
                                        print(mycursor.rowcount, "size_product inserted.")
                                        mydb.close()
                                    except Exception as e:
                                        print(e)
                                        pass
                                else:
                                    pass
                            time.sleep(2)
                    else:
                        pass
                except:
                    pass
            except:
                pass
            data_ += 1
        driver.quit()
    except:
        pass


if __name__ == '__main__':
    fetching_cateogry()
    # Sub_category()
    # Product_Data()