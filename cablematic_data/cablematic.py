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
from cablematic_data.all_functions import *
import mysql.connector
from multiprocessing.pool import ThreadPool


def fetching_category():
    parent_url = 'https://cablematic.com/'
    url = 'https://cablematic.com/en/'
    response = requests.get(url)
    if response.status_code == 200:
        print('Success!')
    elif response.status_code == 404:
        print('PageSoup Not Found.')

    page_soup = BeautifulSoup(response.text , 'html.parser')
    p_id = 0
    cat_id = 0
    try:
        category_div = page_soup.find('div', {'class' : 'row home__banner'})
        category_div_atag = category_div.find_all('a')
        for iteration in category_div_atag:
            category_link = iteration.get('href')
            category_links = urljoin(parent_url , category_link)
            category_name =iteration.find('p').text.strip()
            # category_image = iteration.find('img').get('src')
            # opener = urllib.request.build_opener()
            # opener.addheaders = [('User-Agent',
            #                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
            # urllib.request.install_opener(opener)
            # cat_img_download_func(category_image , category_name)
            print(p_id, category_name , category_links)
            # try:
            #     sql = "INSERT INTO category (category_name,meta_title,meta_description,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
            #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s)"
            #     val = (
            #         category_name, category_name, category_name, "Yes", "Yes", "Yes", p_id,
            #         category_name.replace('-', '').replace('/', '').replace(' ','').strip(), "Yes")
            #     cable_catinsertion(sql, val)
            # except Exception as e:
            #     print('Database query errror')
            #     print(e)
            # response = requests.get('https://cablematic.com/en/products/category/home-and-company/')
            response = requests.get(category_links)
            page_soup = BeautifulSoup(response.text, 'html.parser')
            cat_id = cat_id + 1
            p1_id = cat_id
            try:
                sub_cate_ul = page_soup.find('ul', {'id': 'desktop-menu-level-1'})
                sub_cate_li = sub_cate_ul.find_all('li', {'class': 'category-item selected'})
                for sub_cate_atag in sub_cate_li:
                    sub_cat_div = sub_cate_atag.find('ul', {'class': 'subcategory-list'})
                    sub_cat_links_div = sub_cat_div.find_all('li', {'class': 'subcategory-item'})
                    for sub_cat_atag in sub_cat_links_div:
                        sub_category_link = sub_cat_atag.find('a', {'class': 'subcategory-name'})
                        sub_category_link_ = sub_category_link.get('href')
                        sub_category_links = urljoin(parent_url, sub_category_link_)
                        sub_sub_cat_name = sub_category_link.text.strip()
                        print(p1_id, sub_sub_cat_name, sub_category_links)
                        # try:
                        #     sql = "INSERT INTO category (category_name,meta_title,meta_description,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
                        #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s)"
                        #     val = (
                        #         sub_sub_cat_name, sub_sub_cat_name, sub_sub_cat_name, "Yes", "Yes", "Yes", p1_id,
                        #         sub_sub_cat_name.replace('-', '').replace('/', '').replace(' ', '').strip(), "Yes")
                        #     cable_catinsertion(sql, val)
                        # except Exception as e:
                        #     print('Database query errror')
                        #     print(e)
                        cat_id = cat_id + 1
                        p2_id = cat_id
                        try:
                            driver = runfirfoxOverServer()
                            driver.get(sub_category_links)
                            page_soup = BeautifulSoup(driver.page_source, 'html.parser')

                            sub_sub_cate_ul = page_soup.find('div', {'class': 'subcategory-collapse open'})
                            sub_sub_cate_ul2 = sub_sub_cate_ul.find('ul', {'class': 'subcategory-list'})
                            sub_sub_cate_li = sub_sub_cate_ul2.find_all('li', {'class': 'subcategory-item'})
                            for sub_sub_cat_atag in sub_sub_cate_li:
                                sub_sub_category_link = sub_sub_cat_atag.find('a', {'class': 'subcategory-name'})
                                sub_sub_category_link_ = sub_sub_category_link.get('href')
                                sub_sub_category_links = urljoin(parent_url, sub_sub_category_link_)
                                sub_sub_category_name = sub_sub_category_link.text
                                print(p2_id, sub_sub_category_name,sub_sub_category_links)
                                # try:
                                #     sql = "INSERT INTO category (category_name,meta_title,meta_description,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
                                #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s)"
                                #     val = (
                                #         sub_sub_category_name, sub_sub_category_name, sub_sub_category_name, "Yes", "Yes", "Yes", p2_id,
                                #         sub_sub_category_name.replace('-', '').replace('/', '').replace(' ', '').strip(),
                                #         "Yes")
                                #     cable_catinsertion(sql, val)
                                # except Exception as e:
                                #     print('Database query errror')
                                #     print(e)

                                cat_id = cat_id + 1
                                try:
                                    mydb = mysql.connector.connect(
                                        host="localhost",
                                        user="root",
                                        passwd="",
                                        database="cablematic"
                                    )
                                    mycursor = mydb.cursor()

                                    sql = "SELECT category_id FROM category WHERE category_name ='%s'" % sub_sub_category_name
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
                                        database="cablematic"
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
                                        pagination(sub_sub_category_links, category_id)
                                except:
                                    pass
                        except:
                            pass
                        driver.quit()
            except Exception as e:
                print(e)
                pass

        print("Yahoo Categories End")
        print("Yahoo Categories End")
        print("Yahoo Categories End")
        print("Yahoo Categories End")
    except Exception as e:
        print(e)
        pass

def pagination(sub_sub_category_links , category_id):
    print("Pagination")
    parent_url = 'https://cablematic.com'
    catid = category_id
    url = sub_sub_category_links
    driver = runfirfoxOverServer()
    try:
        driver.get(url)
        driver.implicitly_wait(1)
        page_scroller(driver , 2)
        infinite_scrolling_PageUp(driver,2)
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        page_navigation = page_soup.find('ul', {'class': 'pagination'})                         # pagination
        if page_navigation is not None:
            total_page = page_navigation.find_all('a')
            index_ = len(total_page) - 2
            total_page[index_].text.strip()
            totalpages = total_page[index_].text.strip()
            total_pages = int(totalpages.strip())
            current_url = driver.current_url
            for page_no in range(1, total_pages + 1):
                link = current_url + "?page={0}".format(page_no)
                print(link)
                driver.get(link)
                page_soup = BeautifulSoup(driver.page_source, 'html.parser')
                product_url_list = []
                Allproducts_div = page_soup.find('div',{'id':'content'})
                product_links_div = Allproducts_div.find_all('div',{'class':'product-encapsulate'})
                for iteration in product_links_div:
                    Allproduct_links = iteration.find('a').get('href')
                    product_links = urljoin(parent_url , Allproduct_links)
                    # products_data(product_links, catid)
                    product_url_list.append((product_links,catid))
                multipooling(product_url_list)

        else:
            Allproducts_div = page_soup.find('div', {'id': 'content'})
            product_url_list = []
            product_links_div = Allproducts_div.find_all('div', {'class': 'product-encapsulate'})
            for iteration in product_links_div:
                Allproduct_links = iteration.find('a').get('href')
                product_links = urljoin(parent_url, Allproduct_links)
                # products_data(product_links, catid)
                product_url_list.append((product_links, catid))
            multipooling(product_url_list)
    except:
        pass
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
    driver.quit()

def products_data(chunksList):
    parent_url = 'https://cablematic.com/'
    driver, display = runChromeOverServer()
    for url in chunksList:
        pro_url = url[0]
        cat_id = url[1]
        driver.get(pro_url)
        time.sleep(1)
        try:
            try:
                print("Location Changing")
                driver.find_element_by_xpath('//*[@id="navigator"]/div[1]/div[2]/div/div[3]/ul').click()
                time.sleep(1)
                # WebDriverWait(driver, 5).until(EC.visibility_of_element_located(By.XPATH, '//*[@id="navigator"]/div[1]/div[2]/div/div[3]/ul'))
                print('first clicked')
                driver.find_element_by_xpath('//*[@id="language-picker"]/div[1]/select[1]/option[236]').click()
                print("second Clicked")
                driver.find_element_by_xpath('/html/body/div[3]/div/div/form/div[1]/select[2]/option[2]').click()
                print('Third clicked')
                driver.find_element_by_xpath('//*[@id="language-picker"]/div[2]/button').click()
                print('Location Changed')
            except Exception as e:
                print(e)
                pass

            try:
                time.sleep(1)
                product_title_div = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[2]/h1')
                if product_title_div is not None:
                    product_title = product_title_div.text.strip()
                    print(product_title)
                else:
                    product_title_div = driver.find_element_by_css_selector('body > div.container-fluid.maincontent > div > div.main-content.col-12.col-md-12 > div.row.product.d-none.d-lg-flex > div.col-9.col-xl-8 > div:nth-child(2) > div.col-12.col-lg-7.col-xl-6.product__info > h1')
                    product_title = product_title_div.text.strip()
                    print(product_title)
            except Exception as e:
                print(e)
                pass

            try:
                page_soup = BeautifulSoup(driver.page_source, 'html.parser')
                images_div = page_soup.find('div', {'class': 'carousel slide'})
                try:
                    image_tag = images_div.find_all('div', {'class': 'carousel-item'})[0]
                    if image_tag is not None:
                        for iter_tag in image_tag:
                            images = iter_tag.find('img')
                            product_images = images.get('data-src')
                            print(product_images)
                            opener = urllib.request.build_opener()
                            opener.addheaders = [('User-Agent',
                                                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
                            urllib.request.install_opener(opener)
                            prod_img_download_func(product_images , product_title)
                            print("Image is Downloaded")
                    else:
                        print("Image else")
                        image_tag = images_div.find('div', {'class': 'carousel-item'})
                        images = image_tag.find('img')
                        product_images = images.get('data-src')
                        print(product_images)
                        opener =+ urllib.request.build_opener()
                        opener.addheaders = [('User-Agent',
                                              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
                        urllib.request.install_opener(opener)
                        prod_img_download_func(product_images, product_title)
                        print("Image is Downloaded")
                except:
                    pass
            except Exception as e:
                print(e)
                pass

            try:
                product_price_div = driver.find_element_by_xpath('//*[@id="accordion"]/div[2]/div/div/div[4]/div/h2')
                if product_price_div is not None:
                    product_price = product_price_div.text.strip().replace('£', '').replace(',', '')
                else:
                    product_price_div = driver.find_element_by_css_selector(
                        '#accordion > div.row.price-box.white > div > div > div:nth-child(4) > div > h2')
                    product_price = product_price_div.text.strip().replace('£', '').replace(',', '')
            except Exception as e:
                print(e)
                pass

            try:
                product_description_div = driver.find_element_by_xpath('//*[@id="collapseTwo"]/div')
                product_description = product_description_div.text.replace('Description', '').strip()
                print(product_description)
            except Exception as e:
                print(e)
                pass

            try:
                try:
                    print('1st try')
                    infinite_scrolling_PageDown(driver, 2)
                    driver.find_element_by_css_selector('#headingTwo>a').click()
                except:
                    print('2nd try')
                    infinite_scrolling_PageDown(driver, 1)
                    driver.find_element_by_css_selector('#headingTwo>a').click()
                    print('measurement clicked')
                product_gross = driver.find_element_by_css_selector('#collapseThree')
                product_gross_weight = product_gross.text.strip()
                if product_gross_weight is not None:
                    print("ENtered in Gross weight")
                    product_description = (product_description + product_gross_weight)
                else:
                    pass
            except Exception as e:
                print(e)
                pass

            try:
                time.sleep(1)
                try:
                    driver.find_element_by_css_selector('#headingThree > a').click()
                except:
                    infinite_scrolling_PageDown(driver , 1)
                    driver.find_element_by_css_selector('#headingThree > a').click()

                print('clicked')
                product_documentation = driver.find_element_by_css_selector('#collapseFour')
                product_documentation_links = product_documentation.find_elements_by_tag_name('a')
                for options in product_documentation_links:
                    product_documentation_urls = options.get_attribute('href')
                    print(product_documentation_urls)
                    if product_documentation_urls is not None:
                        product_description = (product_description + product_gross_weight + ' \n For Further Details in PDF: ' + product_documentation_urls)
                        print('document click')
                    else:
                        pass
            except:
                pass
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="cablematic"
                )

                mycursor = mydb.cursor()

                sql = "INSERT INTO products (product_name,product_description,meta_title,meta_description,meta_keywords,status,category_id,feature_image,IsHome,IsFeature,IsSpecial,product_url,pro_price)" \
                      " VALUES (%s, %s,%s, %s, %s,%s, %s,%s,%s,%s,%s,%s,%s)"
                val = (
                    product_title, product_description, product_title,
                    product_title, product_title, "Yes", cat_id,
                    str(product_title).lower().replace(',', '').replace('-', '').replace(' ', '').replace('/', '').replace('(','').replace(')','')+'.jpg',
                    'Yes',
                    'Yes', 'Yes', product_title.replace('-', '').replace(',', '').replace('@', '').replace(' ', '').replace('(','').replace(')','').strip(),
                    product_price)
                mycursor.execute(sql, val)

                mydb.commit()

                print(mycursor.rowcount, "product inserted.")
                mydb.close()
            except Exception as e:
                print("Product not inserted")
                print(e)

            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="cablematic"
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

            try:
                page_soup = BeautifulSoup(driver.page_source, 'html.parser')
                images_div = page_soup.find('div', {'class': 'carousel slide'})
                image_tag = images_div.find_all('div', {'class': 'carousel-item'})
                if image_tag is not None:
                    z = 0
                    for iter_tag in image_tag:
                        images = iter_tag.find('img')
                        product_images = images.get('data-src')
                        multiple_images = (product_title + str(z) + '.jpg')
                        opener = urllib.request.build_opener()
                        opener.addheaders = [('User-Agent',
                                              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
                        urllib.request.install_opener(opener)
                        multi_prod_img_download_func(product_images, product_title, z)
                        print("Image is Downloaded")
                        print(multiple_images)
                        try:
                            mydb = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                passwd="",
                                database="cablematic"
                            )
                            mycursor = mydb.cursor()

                            sql = "INSERT INTO products_images (product_id,image_file)" \
                                  " VALUES (%s,%s)"
                            val = (product_id,
                                   str(multiple_images).lower().replace(',', '').replace('-', '').replace('/', '').replace(
                                       '@', '').replace(' ', '').replace('(','').replace(')',''))
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
                pass

            try:
                size_id = 0
                infinite_scrolling_PageUp(driver, 5)
                try:
                    driver.find_element_by_css_selector('#headingOne > h5 > button').click()
                    print("variation button clicked")
                except:
                    pass
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                time.sleep(1)
                pro_variation_div = soup.find('div', {'class': 'col-3 col-xl-2 mt-auto mb-auto'})
                if pro_variation_div is not None:
                    print("Entered in Variations")
                    pro_variation_div_atag = pro_variation_div.find('a')
                    variation_link = pro_variation_div_atag.get('href')
                    pro_variation_links = urljoin(parent_url, variation_link)
                    driver.get(pro_variation_links)
                    try:
                        product_price_div = driver.find_element_by_xpath(
                            '//*[@id="accordion"]/div[2]/div/div/div[4]/div/h2')
                        if product_price_div is not None:
                            product_price = product_price_div.text.strip().replace('£', '').replace(',', '')
                        else:
                            product_price_div = driver.find_element_by_css_selector(
                                '#accordion > div.row.price-box.white > div > div > div:nth-child(4) > div > h2')
                            product_price = product_price_div.text.strip().replace('£', '').replace(',', '')
                    except Exception as e:
                        print(e)
                        pass
                    try:
                        product_title_div = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[2]/h1')
                        if product_title_div is not None:
                            product_title = product_title_div.text.replace(',', '').replace('-', '').replace(' ', '').replace('/', '').replace('(','').replace(')','').strip()
                        else:
                            product_title_div = driver.find_element_by_css_selector('body > div.container-fluid.maincontent > div > div.main-content.col-12.col-md-12 > div.row.product.d-none.d-lg-flex > div.col-9.col-xl-8 > div:nth-child(2) > div.col-12.col-lg-7.col-xl-6.product__info > h1')
                            product_title = product_title_div.text.replace(',', '').replace('-', '').replace(' ', '').replace('/', '').replace('(','').replace(')','').strip()
                    except Exception as e:
                        print(e)
                        pass

                    try:
                        mydb = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            passwd="",
                            database="cablematic"
                        )
                        mycursor = mydb.cursor()

                        sql = "INSERT INTO products_size(size_id,product_id, price,size)" \
                              " VALUES (%s,%s,%s,%s)"
                        val = (size_id, product_id, product_price, product_title.replace(',','').replace('/','').replace('@','').replace('-','').replace('(','').replace(')',''))
                        mycursor.execute(sql, val)
                        mydb.commit()
                        print(mycursor.rowcount, "size_product inserted.")
                        mydb.close()
                    except Exception as e:
                        print(e)
                        pass
                    size_id+=1
                else:
                    print("No Variation in this product")
            except:
                traceback.print_exc()
                pass
        except:
            traceback.print_exc()
            print("Error In Url" , pro_url)
            pass
    driver.close()
    driver.quit()

if __name__ == '__main__':
    fetching_category()
