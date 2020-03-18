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
from Vicking.viking_all_functions import *
import mysql.connector
from multiprocessing.pool import ThreadPool

def fetching_categories():
    parent_url = "https://www.vikingtapes.co.uk/"
    try:
        response = requests.get(parent_url)
        time.sleep(1)
        page_soup = BeautifulSoup(response.text , 'html.parser')
        p_id = 0
        cat_id = 0
        main_category_div = page_soup.find("div",{"class" , "featCollections"})
        main_category_tag = main_category_div.find_all("div", {"class", "grid__item large--one-third medium--one-half"})
        for atags in main_category_tag:
            main_cate_name = atags.find("a",{"class","featCollections__title"}).text.strip()
            main_cate_url = urljoin(parent_url , atags.find("a",{"class","featCollections__title"}).get('href'))
            # main_cat_image = atags.find("img",{"class","collectionProductImage"}).get('data-src')
            # if main_cat_image is not None:
            #     cat_img_download_func(urljoin(parent_url,main_cat_image),main_cate_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",'').strip())
            # else:
            #     pass
            print(p_id, "main_cactegory:" ,main_cate_name , main_cate_url)
            # try:
            #     sql = "INSERT INTO category (category_name,meta_title,meta_description,category_image,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
            #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s,%s)"
            #     val = (main_cate_name, main_cate_name, main_cate_name, main_cate_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",'').strip()+".jpg","Yes", "Yes", "Yes", p_id,
            #            main_cate_name.replace('-', '').replace('/', '').replace(' ','').replace('@','').strip(), "Yes")
            #     cat_data_insertion(sql, val)
            # except Exception as e:
            #     print('Database query errror')
            #     print(e)

            try:
                response = requests.get(main_cate_url)
                time.sleep(1)
                page_soup = BeautifulSoup(response.text, 'html.parser')
                cat_id = cat_id + 1
                p1_id = cat_id
                sub_category_div = page_soup.find("div", {"class", "featCollections"})
                if sub_category_div:
                    sub_category_tag = sub_category_div.find_all("div",{"class", "grid__item large--one-third medium--one-half"})
                    for atags in sub_category_tag:
                        sub_cate_name = atags.find("a", {"class", "featCollections__title"}).text.strip()
                        sub_cate_url = urljoin(parent_url, atags.find("a", {"class", "featCollections__title"}).get('href'))
                        # try:
                        #     sub_cat_image = atags.find("img", {"class", "collectionProductImage"}).get('src')
                        #     if sub_cat_image is not None:
                        #         sub_cat_img_download_func(urljoin(parent_url, sub_cat_image), sub_cate_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",'')).strip()
                        #     else:
                        #         pass
                        # except:
                        #     pass
                        print(p1_id,"1st sub_category", sub_cate_name, sub_cate_url)
                        # try:
                        #     sql = "INSERT INTO category (category_name,meta_title,meta_description,category_image,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
                        #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s,%s)"
                        #     val = (sub_cate_name, sub_cate_name, sub_cate_name,sub_cate_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",'').strip()+".jpg", "Yes", "Yes", "Yes", p1_id,
                        #            sub_cate_name.replace('-', '').replace('/', '').replace(' ', '').replace('@','').strip(),"Yes")
                        #     cat_data_insertion(sql, val)
                        # except Exception as e:
                        #     print('Database query errror')
                        #     print(e)

                        try:
                            response = requests.get(sub_cate_url)
                            time.sleep(1)
                            page_soup = BeautifulSoup(response.text, 'html.parser')
                            cat_id = cat_id + 1
                            p2_id = cat_id
                            sub_sub_category_div = page_soup.find("div", {"class", "featCollections"})
                            if sub_sub_category_div:
                                sub_sub_category_tag = sub_sub_category_div.find_all("div", {"class","grid__item large--one-third medium--one-half"})
                                for atags in sub_sub_category_tag:
                                    sub_sub_cate_name = atags.find("a", {"class", "featCollections__title"}).text.strip()
                                    sub_sub_cate_url = urljoin(parent_url,atags.find("a", {"class", "featCollections__title"}).get('href'))
                                    # try:
                                    #     sub_sub_cat_image = atags.find("img", {"class", "collectionProductImage"}).get('src')
                                    #     if sub_sub_cat_image is not None:
                                    #         sub_cat_img_download_func(urljoin(parent_url, sub_sub_cat_image), sub_sub_cate_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",''))
                                    #     else:
                                    #         pass
                                    # except:
                                    #     pass
                                    if sub_sub_cate_url != parent_url:
                                        print(p2_id,"2nd sub_category", sub_sub_cate_name, sub_sub_cate_url)
                                        # try:
                                        #     sql = "INSERT INTO category (category_name,meta_title,meta_description,category_image,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
                                        #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s,%s)"
                                        #     val = (
                                        #     sub_sub_cate_name, sub_sub_cate_name, sub_sub_cate_name,sub_sub_cate_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",'').strip()+".jpg", "Yes", "Yes", "Yes", p2_id,
                                        #     sub_sub_cate_name.replace('-', '').replace('/', '').replace(' ', '').replace(
                                        #         '@', '').strip(), "Yes")
                                        #     cat_data_insertion(sql, val)
                                        # except Exception as e:
                                        #     print('Database query errror')
                                        #     print(e)
                                    else:
                                        pass

                                    try:
                                        # response = requests.get("https://www.vikingtapes.co.uk/collections/3m-vhb-tapes")
                                        response = requests.get(sub_sub_cate_url)
                                        time.sleep(1)
                                        page_soup = BeautifulSoup(response.text, 'html.parser')
                                        cat_id = cat_id + 1
                                        p3_id = cat_id
                                        sub_sub_sub_category_div = page_soup.find("div", {"class", "featCollections"})
                                        if sub_sub_sub_category_div:
                                            sub_sub_sub_category_tag = sub_sub_sub_category_div.find_all("div", {"class","grid__item large--one-third medium--one-half"})
                                            for atags in sub_sub_sub_category_tag:
                                                sub_sub_sub_cate_name = atags.find("a", {"class","featCollections__title"}).text.strip()
                                                sub_sub_sub_cate_url = urljoin(parent_url, atags.find("a", {"class","featCollections__title"}).get('href'))
                                                # try:
                                                #     sub_sub_sub_cat_image = atags.find("img",{"class", "collectionProductImage"}).get('src')
                                                #     if sub_sub_sub_cat_image is not None:
                                                #         sub_cat_img_download_func(urljoin(parent_url, sub_sub_sub_cat_image),sub_sub_sub_cate_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",''))
                                                #     else:
                                                #         pass
                                                # except:
                                                #     pass
                                                if sub_sub_sub_cate_url != parent_url:
                                                    print(p3_id,"3rd sub_category", sub_sub_sub_cate_name, sub_sub_sub_cate_url)
                                                    # try:
                                                    #     sql = "INSERT INTO category (category_name,meta_title,meta_description,category_image,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
                                                    #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s,%s)"
                                                    #     val = (sub_sub_sub_cate_name, sub_sub_sub_cate_name, sub_sub_sub_cate_name,sub_sub_sub_cate_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",'').strip()+".jpg", "Yes",
                                                    #         "Yes", "Yes", p3_id,
                                                    #         sub_sub_sub_cate_name.replace('-', '').replace('/', '').replace(' ','').replace('@', '').strip(), "Yes")
                                                    #     cat_data_insertion(sql, val)
                                                    # except Exception as e:
                                                    #     print('Database query errror')
                                                    #     print(e)
                                                else:
                                                    pass

                                                try:
                                                    # response = requests.get("https://www.vikingtapes.co.uk/collections/3m-vhb-tape-reference-numbers")
                                                    # response = requests.get("https://www.vikingtapes.co.uk/collections/3m-vhb-tapes")
                                                    response = requests.get(sub_sub_sub_cate_url)
                                                    time.sleep(1)
                                                    soup = BeautifulSoup(response.text, 'html.parser')
                                                    cat_id = cat_id + 1
                                                    p4_id = cat_id
                                                    final_sub_category_div = soup.find("div",{"class", "featCollections"})
                                                    if final_sub_category_div:
                                                        final_sub_category_tag = final_sub_category_div.find_all("div",{"class","grid__item large--one-third medium--one-half"})
                                                        if final_sub_category_tag:
                                                            print("Entered in final sub_category")
                                                            for atags in final_sub_category_tag:
                                                                final_sub_cate_name = atags.find("a", {"class", "featCollections__title"}).text.strip()
                                                                final_sub_cate_url = urljoin(parent_url, atags.find("a",{"class","featCollections__title"}).get('href'))
                                                                # try:
                                                                #     sub_cat_image = atags.find("img", {"class","collectionProductImage"}).get('src')
                                                                #     if sub_cat_image is not None:
                                                                #         sub_cat_img_download_func(urljoin(parent_url, sub_cat_image),final_sub_cate_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",''))
                                                                #     else:
                                                                #         pass
                                                                # except:
                                                                #     pass
                                                                if final_sub_cate_url != parent_url:
                                                                    print(p4_id,"if final sub_category", final_sub_cate_name,final_sub_cate_url)
                                                                    # try:
                                                                    #     sql = "INSERT INTO category (category_name,meta_title,meta_description,category_image,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
                                                                    #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s,%s)"
                                                                    #     val = (final_sub_cate_name, final_sub_cate_name,final_sub_cate_name,final_sub_cate_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",'').strip()+".jpg", "Yes","Yes", "Yes", p4_id,
                                                                    #         final_sub_cate_name.replace('-', '').replace('/', '').replace(' ', '').replace('@','').strip(),
                                                                    #         "Yes")
                                                                    #     cat_data_insertion(sql, val)
                                                                    # except Exception as e:
                                                                    #     print('Database query errror')
                                                                    #     print(e)
                                                                    cat_id = cat_id + 1
                                                                    try:
                                                                        categorylist = []
                                                                        mydb = mysql.connector.connect(
                                                                            host="localhost",
                                                                            user="root",
                                                                            passwd="",
                                                                            database="vicking"
                                                                        )
                                                                        mycursor = mydb.cursor()

                                                                        sql = "SELECT category_id FROM category WHERE category_name ='%s'" % final_sub_cate_name
                                                                        mycursor.execute(sql)
                                                                        myresult = mycursor.fetchall()
                                                                        for x in myresult:
                                                                            category_id = x[0]
                                                                            categorylist.append(category_id)
                                                                        print(categorylist)
                                                                    except Exception as e:
                                                                        print(e)
                                                                        pass
                                                                    try:
                                                                        catelist = []
                                                                        mydb = mysql.connector.connect(
                                                                            host="localhost",
                                                                            user="root",
                                                                            passwd="",
                                                                            database="vicking"
                                                                        )
                                                                        mycursor = mydb.cursor()
                                                                        sql = "SELECT category_id FROM products"
                                                                        mycursor.execute(sql)
                                                                        myresult = mycursor.fetchall()
                                                                        for x in myresult:
                                                                            cat_id = x[0]
                                                                            catelist.append(cat_id)
                                                                        for category_id_ in categorylist:
                                                                            if category_id_ in catelist:
                                                                                pass
                                                                                print("Already Exist in Database")
                                                                            else:
                                                                                ExtractProductUrls(final_sub_cate_url,
                                                                                                   category_id_)
                                                                    except:
                                                                        pass
                                                                else:
                                                                    pass


                                                        else:
                                                            final_sub_category_table_ = soup.find("table")
                                                            final_sub_category_div = final_sub_category_table_.find_all( "tr")[1:]
                                                            if final_sub_category_div:
                                                                for iteration in final_sub_category_div:
                                                                    final_sub_category_links = iteration.find_all('a')
                                                                    for ahref in final_sub_category_links:
                                                                        final_sub_cate_url = ahref.get('href')
                                                                        final_sub_cate_name = ahref.text.strip()
                                                                        if final_sub_cate_url != parent_url:
                                                                            print(p4_id,"Else Final Sub Category:",final_sub_cate_name,final_sub_cate_url)
                                                                            # try:
                                                                            #     sql = "INSERT INTO category (category_name,meta_title,meta_description,status,IsHome,IsMenu,parent,category_url,gfeed_status)" \
                                                                            #           " VALUES (%s, %s,%s, %s,%s, %s, %s,%s, %s)"
                                                                            #     val = (
                                                                            #     final_sub_cate_name, final_sub_cate_name,final_sub_cate_name, "Yes", "Yes", "Yes",p4_id,
                                                                            #     final_sub_cate_name.replace('-','').replace('/','').replace(    ' ', '').replace('@', '').strip(),
                                                                            #     "Yes")
                                                                            #     cat_data_insertion(sql, val)
                                                                            # except Exception as e:
                                                                            #     print('Database query errror')
                                                                            #     print(e)
                                                                            cat_id = cat_id + 1
                                                                            try:
                                                                                categorylist = []
                                                                                mydb = mysql.connector.connect(
                                                                                    host="localhost",
                                                                                    user="root",
                                                                                    passwd="",
                                                                                    database="vicking"
                                                                                )
                                                                                mycursor = mydb.cursor()

                                                                                sql = "SELECT category_id FROM category WHERE category_name ='%s'" % final_sub_cate_name
                                                                                mycursor.execute(sql)
                                                                                myresult = mycursor.fetchall()
                                                                                for x in myresult:
                                                                                    category_id = x[0]
                                                                                    categorylist.append(category_id)
                                                                                print(categorylist)
                                                                            except Exception as e:
                                                                                print(e)
                                                                                pass
                                                                            try:
                                                                                catelist = []
                                                                                mydb = mysql.connector.connect(
                                                                                    host="localhost",
                                                                                    user="root",
                                                                                    passwd="",
                                                                                    database="vicking"
                                                                                )
                                                                                mycursor = mydb.cursor()
                                                                                sql = "SELECT category_id FROM products"
                                                                                mycursor.execute(sql)
                                                                                myresult = mycursor.fetchall()
                                                                                for x in myresult:
                                                                                    cat_id = x[0]
                                                                                    catelist.append(cat_id)
                                                                                for category_id_ in categorylist:
                                                                                    if category_id_ in catelist:
                                                                                        pass
                                                                                        print(
                                                                                            "Already Exist in Database")
                                                                                    else:
                                                                                        ExtractProductUrls(
                                                                                            final_sub_cate_url,
                                                                                            category_id_)
                                                                            except:
                                                                                pass
                                                                        else:
                                                                            pass
                                                            else:
                                                                print("No More Data",)
                                                                pass

                                                    else:
                                                        print("Else 3rd sub_category", sub_sub_sub_cate_name,sub_sub_sub_cate_url)
                                                        final_sub_cate_url = sub_sub_sub_cate_url
                                                        try:
                                                            categorylist = []
                                                            mydb = mysql.connector.connect(
                                                                host="localhost",
                                                                user="root",
                                                                passwd="",
                                                                database="vicking"
                                                            )
                                                            mycursor = mydb.cursor()

                                                            sql = "SELECT category_id FROM category WHERE category_name ='%s'" % sub_sub_sub_cate_name
                                                            mycursor.execute(sql)
                                                            myresult = mycursor.fetchall()
                                                            for x in myresult:
                                                                category_id = x[0]
                                                                categorylist.append(category_id)
                                                            print(categorylist)
                                                        except Exception as e:
                                                            print(e)
                                                            pass
                                                        try:
                                                            catelist = []
                                                            mydb = mysql.connector.connect(
                                                                host="localhost",
                                                                user="root",
                                                                passwd="",
                                                                database="vicking"
                                                            )
                                                            mycursor = mydb.cursor()
                                                            sql = "SELECT category_id FROM products"
                                                            mycursor.execute(sql)
                                                            myresult = mycursor.fetchall()
                                                            for x in myresult:
                                                                cat_id = x[0]
                                                                catelist.append(cat_id)
                                                            for category_id_ in categorylist:
                                                                if category_id_ in catelist:
                                                                    pass
                                                                    print("Already Exist in Database")
                                                                else:
                                                                    ExtractProductUrls(final_sub_cate_url, category_id_)
                                                        except:
                                                            pass
                                                except:
                                                    traceback.print_exc()
                                                    pass

                                        else:
                                            print("2nd sub_category", sub_sub_cate_name, sub_sub_cate_url)
                                            final_sub_cate_url = sub_sub_cate_url
                                            try:
                                                categorylist = []
                                                mydb = mysql.connector.connect(
                                                    host="localhost",
                                                    user="root",
                                                    passwd="",
                                                    database="vicking"
                                                )
                                                mycursor = mydb.cursor()

                                                sql = "SELECT category_id FROM category WHERE category_name ='%s'" % sub_sub_cate_name
                                                mycursor.execute(sql)
                                                myresult = mycursor.fetchall()
                                                for x in myresult:
                                                    category_id = x[0]
                                                    categorylist.append(category_id)
                                                print(categorylist)
                                            except Exception as e:
                                                print(e)
                                                pass
                                            try:
                                                catelist = []
                                                mydb = mysql.connector.connect(
                                                    host="localhost",
                                                    user="root",
                                                    passwd="",
                                                    database="vicking"
                                                )
                                                mycursor = mydb.cursor()
                                                sql = "SELECT category_id FROM products"
                                                mycursor.execute(sql)
                                                myresult = mycursor.fetchall()
                                                for x in myresult:
                                                    cat_id = x[0]
                                                    catelist.append(cat_id)
                                                for category_id_ in categorylist:
                                                    if category_id_ in catelist:
                                                        pass
                                                        print("Already Exist in Database")
                                                    else:
                                                        ExtractProductUrls(final_sub_cate_url, category_id_)
                                            except:
                                                pass
                                    except:
                                        traceback.print_exc()
                                        pass
                            else:
                                print("Else 1st sub_category", sub_cate_name, sub_cate_url)
                                final_sub_cate_url = sub_cate_url
                                try:
                                    categorylist = []
                                    mydb = mysql.connector.connect(
                                        host="localhost",
                                        user="root",
                                        passwd="",
                                        database="vicking"
                                    )
                                    mycursor = mydb.cursor()

                                    sql = "SELECT category_id FROM category WHERE category_name ='%s'" % sub_cate_name
                                    mycursor.execute(sql)
                                    myresult = mycursor.fetchall()
                                    for x in myresult:
                                        category_id = x[0]
                                        categorylist.append(category_id)
                                    print(categorylist)
                                except Exception as e:
                                    print(e)
                                    pass
                                try:
                                    catelist = []
                                    mydb = mysql.connector.connect(
                                        host="localhost",
                                        user="root",
                                        passwd="",
                                        database="vicking"
                                    )
                                    mycursor = mydb.cursor()
                                    sql = "SELECT category_id FROM products"
                                    mycursor.execute(sql)
                                    myresult = mycursor.fetchall()
                                    for x in myresult:
                                        cat_id = x[0]
                                        catelist.append(cat_id)
                                    for category_id_ in categorylist:
                                        if category_id_ in catelist:
                                            pass
                                            print("Already Exist in Database")
                                        else:
                                            ExtractProductUrls(final_sub_cate_url, category_id_)
                                except:
                                    pass
                        except:
                            traceback.print_exc()
                else:
                    print("else main_category", main_cate_name, main_cate_url)
            except:
                traceback.print_exc()
                pass

        print("Yahoo categories end")
        print("Yahoo categories end")
        print("Yahoo categories end")
    except:
        traceback.print_exc()
        pass

def ExtractProductUrls(final_sub_cate_url, category_id_):
    parent_url = "https://www.vikingtapes.co.uk/"
    try:
        response = requests.get(final_sub_cate_url)
        time.sleep(1)
        page_soup = BeautifulSoup(response.text, 'html.parser')
        product_url_div = page_soup.find("div", {"class", "grid-uniform"})
        if product_url_div:
            product_url_tag = product_url_div.find_all("div", {"class", "grid__item large--one-third medium--one-half"})
            product_url_list = []
            for atags in product_url_tag:
                product_url_ = atags.find("a", {"class", "grid__image"}).get("href")
                if product_url_:
                    product_url =urljoin(parent_url , product_url_)
                    product_url_list.append((category_id_ , product_url))
                else:
                    pass
            print(product_url_list)
            multipooling(product_url_list)
        else:
            productUrl_div = page_soup.find("div", {"class", "featCollections"})
            if productUrl_div:
                product_urls_tag = productUrl_div.find_all("div",{"class", "grid__item large--one-third medium--one-half"})
                for atags in product_urls_tag:
                    product_urls_last = urljoin(parent_url,atags.find("a", {"class", "featCollections__title"}).get('href'))
                    response = requests.get(product_urls_last)
                    page_soup = BeautifulSoup(response.text, 'html.parser')
                    product_url_div = page_soup.find("div", {"class", "grid-uniform"})
                    if product_url_div:
                        product_url_tag = product_url_div.find_all("div", {"class","grid__item large--one-third medium--one-half"})
                        product_url_list = []
                        for atags in product_url_tag:
                            product_url_ = atags.find("a", {"class", "grid__image"}).get("href")
                            if product_url_:
                                product_url = urljoin(parent_url, product_url_)
                                product_url_list.append((category_id_, product_url))
                            else:
                                pass
                        print(product_url_list)
                        multipooling(product_url_list)
                    else:
                        productUrl_div = page_soup.find("div", {"class", "featCollections"})
                        product_urls_tag = productUrl_div.find_all("div", {"class","grid__item large--one-third medium--one-half"})
                        for atags in product_urls_tag:
                            product_urls_last = urljoin(parent_url,atags.find("a", {"class", "featCollections__title"}).get('href'))
                            response = requests.get(product_urls_last)
                            page_soup = BeautifulSoup(response.text, 'html.parser')
                            product_url_div = page_soup.find("div", {"class", "grid-uniform"})
                            if product_url_div:
                                product_url_tag = product_url_div.find_all("div", {"class","grid__item large--one-third medium--one-half"})
                                product_url_list = []
                                for atags in product_url_tag:
                                    product_url_ = atags.find("a", {"class", "grid__image"}).get("href")
                                    if product_url_:
                                        product_url = urljoin(parent_url, product_url_)
                                        product_url_list.append((category_id_, product_url))
                                    else:
                                        pass
                                print(product_url_list)
                                multipooling(product_url_list)
                            else:
                                final_sub_category_table_ = page_soup.find("table")
                                final_sub_category_div = final_sub_category_table_.find_all("tr")[1:]
                                if final_sub_category_div:
                                    product_url_list = []
                                    for iteration in final_sub_category_div:
                                        final_sub_category_links = iteration.find_all('a')
                                        for ahref in final_sub_category_links:
                                            product_url = ahref.get('href')
                                            if product_url != parent_url:
                                                print("Product_Urls", product_url)
                                                product_url_list.append((category_id_, product_url))
                                        multipooling(product_url_list)
                                else:
                                    pass
            else:
                pass

    except Exception as e:
        print(e)

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
    pool_size = 4
    pool = ThreadPool(pool_size)
    pool.map(ExtractProductData, chunksList)
    pool.close()
    pool.join()
    print('Done All Pool')

def ExtractProductData(chunksList):
    parent_url = 'https://cablematic.com/'
    for url in chunksList:
        pro_url = url[1]
        cat_id = url[0]
        try:
            response = requests.get(pro_url)
            time.sleep(1)
            page_soup = BeautifulSoup(response.text, 'html.parser')
            try:
                product_title = page_soup.find('h1', {'class': 'product__title'}).text.strip()
                print(product_title)
            except:
                traceback.print_exc()
            if product_title:
                try:
                    print("product pro")
                    product_price_ = page_soup.find('span', {'id': 'PreTaxProductPrice'}).text
                    product_price = product_price_.replace('Only','').replace(',','').replace('£', '').strip()
                    print(product_price)
                except:
                    traceback.print_exc()
                try:
                    product_description_pdf_div = page_soup.find("p",{'class': 'sidebar-product'})
                    product_description_pdf = product_description_pdf_div.find('a').get("href")
                    if product_description_pdf:
                        parent_tag = "https:"
                        pdf_link = urljoin(parent_tag, product_description_pdf)
                    else:
                        pass
                except:
                    traceback.print_exc()

                try:
                    product_description_div=page_soup.find("div",{"class": 'product-description rte'})
                    product_description_tag = product_description_div.text.strip()
                    if pdf_link != None:
                        product_description = product_description_tag + "\nFor more Details: " + pdf_link
                        print("If tag ", product_description)
                    else:
                        print("Else Description")
                        product_description = product_description_tag
                        print(product_description)
                except:
                    traceback.print_exc()

                try:
                    product_image_div = page_soup.find('div',{'id': 'ProductPhoto'})
                    product_image = urljoin("https:", product_image_div.find('img').get('src'))
                    prod_img_download_func(product_image , product_title.lower().replace('@','').replace('/','').replace('-','').replace(',',''))
                except:
                    traceback.print_exc()

                try:
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        passwd="",
                        database="vicking"
                    )

                    mycursor = mydb.cursor()

                    sql = "INSERT INTO products (product_name,product_description,meta_title,meta_description,meta_keywords,status,category_id,feature_image,IsHome,IsFeature,IsSpecial,product_url,pro_price)" \
                          " VALUES (%s, %s,%s, %s, %s,%s, %s,%s,%s,%s,%s,%s,%s)"
                    val = (
                        product_title, product_description, product_title,
                        product_title, product_title, "Yes", cat_id,
                        str(product_title).lower().replace(',', '').replace('-', '').replace(' ', '').replace('/', '').replace('(', '').replace(')', '') + '.jpg',
                        'Yes',
                        'Yes', 'Yes',
                        product_title.replace('-', '').replace(',', '').replace('@', '').replace(' ', '').replace('(','').replace(')', '').strip(),
                        product_price)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print(mycursor.rowcount, "product inserted.")
                    mydb.close()
                except Exception as e:
                    print("Product not inserted")
                    print(e)
            else:
                product_url_div = page_soup.find("div", {"class", "grid-uniform"})
                if product_url_div:
                    product_url_tag = product_url_div.find_all("div", {"class",
                                                                       "grid__item large--one-third medium--one-half"})
                    product_url_list = []
                    for atags in product_url_tag:
                        product_url_ = atags.find("a", {"class", "grid__image"}).get("href")
                        if product_url_:
                            product_url = urljoin(parent_url, product_url_)
                            product_url_list.append((cat_id, product_url))
                        else:
                            pass
                    print(product_url_list)
                    multipooling(product_url_list)
                else:
                    pass
        except:
            traceback.print_exc()
            pass

def beautifulsoup_categories():
    response = requests.get("https://www.vikingtapes.co.uk/")
    page_soup = BeautifulSoup(response.text , 'html.parser')
    main_category_div = page_soup.find("div",{"class" , "featCollections"})
    main_category_tag = main_category_div.find_all("div", {"class", "grid__item large--one-third medium--one-half"})
    for atags in main_category_tag:
        main_cate_url = atags.find("a",{"class","featCollections__title"})
        print(main_cate_url)

def selenium_categories():
    driver = runfirfoxOverServer()
    driver.get("https://www.vikingtapes.co.uk/")
    delay = 1
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME,"featCollections")))
    print("Page is Ready Now")
    main_category_div = driver.find_element_by_css_selector("#PageContainer > div > div > div > main > div > div.grid__item.large--seven-twelfths > div > div.featCollections > div > div:nth-child(1)")
    print(main_category_div.text)

if __name__ == '__main__':
    fetching_categories()
