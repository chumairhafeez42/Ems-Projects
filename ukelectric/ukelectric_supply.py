from ukelectric.uk_all_function import *
import mysql.connector
from bs4 import BeautifulSoup
import traceback
import time
from urllib.parse import urljoin

#<------------------------------Fetching_categories------------------------------------->
def fetching_main_cats():
    driver = runfirfoxOverServer()
    parent_url = 'https://www.ukelectricalsupplies.com/'
    try:
        driver.get(parent_url)
        time.sleep(1)
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        main_cate_ul = page_soup.find('ul',{'class': 'menuTemplate3 decor3_1'})
        main_cate_links = main_cate_ul.find_all('div',{'id': 'nav_item'})[:-1]
        p_id = 0
        cat_id = 0
        for cate_urls in main_cate_links:
            category_urls = cate_urls.find('a').get('href')
            main_category_name =  cate_urls.find('a').text.replace('&','').strip()
            print("main category: ",p_id,main_category_name,category_urls)
            #######------------Fetching subcategories--------------------------########

            driver.get(category_urls)
            time.sleep(1)
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            try:
                cat_image_div = page_soup.find('div',{'class': 'catmain'})
                cate_image = cat_image_div.find('img').get('src')
            #     if cate_image is not None:
            #         pass
            #         cat_img_download_func(cate_image, main_category_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",''))
            #         # print("main_category_image: " ,str(main_category_image))
            #     else:
            #         pass
            except:
                pass
            # try:
            #     val = (
            #         main_category_name, main_category_name, main_category_name,
            #         main_category_name.replace(' ', '')+'.jpg', "Yes", "Yes", "Yes", p_id,
            #         main_category_name.replace('-', '').replace('/', '').replace(' ','').strip(), "Yes")
            #     cat_data_insertion(val)
            # except Exception as e:
            #     print('Database query errror')
            #     print(e)

            cat_id = cat_id + 1
            p1_id=cat_id

            scnd_category_div = page_soup.find('div', {'class': 'prod_cat_wrapper'})
            sub_cate_div = scnd_category_div.find_all('div',{'class': 'fcont'})[1:]
            for sub_cat_nav in sub_cate_div:
                sub_cats_span = sub_cat_nav.find('span', {'class': 'img va-product-img'})
                sub_category_urls = urljoin(parent_url , sub_cats_span.find('a').get('href'))
                sub_category_name = sub_cats_span.find('img').get('alt')
                # sub_cate_img  = sub_cats_span.find('img').get('src')
                # if sub_cate_img is not None:
                #     sub_cat_img_download_func(sub_cate_img,sub_category_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",''))
                # else:
                #     pass
                print("1st sub_category",p1_id, sub_category_name, sub_category_urls)
                # try:
                #     val = (
                #         sub_category_name, sub_category_name, sub_category_name,
                #         sub_category_name.replace(' ', '').replace('-','').replace('/','')+'.jpg', "Yes", "Yes", "Yes", p1_id,
                #         sub_category_name.replace('-','').replace('/','').replace(' ','').strip(), "Yes")
                #     cat_data_insertion(val)
                # except Exception as e:
                #     print(e)

                cat_id = cat_id+1
                p2_id = cat_id

                #######------------Fetching inner_subcategories--------------------------########

                driver.get(sub_category_urls)
                time.sleep(1)
                page_soup = BeautifulSoup(driver.page_source, 'html.parser')
                inner_category_div = page_soup.find('div', {'class': 'prod_cat_wrapper'})
                if inner_category_div is not None:
                    inner_sub_cate_div = inner_category_div.find_all('div', {'class': 'fcont'})
                    for sub_cat_nav in inner_sub_cate_div:
                        sub_cats_span = sub_cat_nav.find('span', {'class': 'img va-product-img'})
                        inner_sub_category_urls = urljoin(parent_url, sub_cats_span.find('a').get('href'))
                        inner_sub_category_name = sub_cats_span.find('img').get('alt')
                        # inner_sub_cate_img = sub_cats_span.find('img').get('src')
                        # if inner_sub_cate_img is not None:
                        #     sub_cat_img_download_func(inner_sub_cate_img,inner_sub_category_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",''))
                        # else:
                        #     pass
                        #
                        print("Inner_Sub_Category: ",p2_id,inner_sub_category_name, inner_sub_category_urls)
                        # try:
                        #     val = (
                        #         inner_sub_category_name, inner_sub_category_name, inner_sub_category_name,
                        #         inner_sub_category_name.replace(' ', '').replace('-','').replace('/','')+'.jpg', "Yes", "Yes", "Yes", p2_id,
                        #         inner_sub_category_name.replace('-','').replace('/','').replace(' ','').strip(), "Yes")
                        #     cat_data_insertion(val)
                        # except Exception as e:
                        #     print(e)

                        cat_id = cat_id + 1
                        p3_id = cat_id

                                #     #######------------Fetching final_subcategories--------------------------########
                        try:
                            driver.get(inner_sub_category_urls)
                            time.sleep(1)
                            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
                            final_category_div = page_soup.find('div', {'class': 'prod_cat_wrapper'})
                            if final_category_div is not None:
                                final_sub_cate_div = final_category_div.find_all('div', {'class': 'fcont'})
                                for sub_cat_nav in final_sub_cate_div:
                                    sub_cats_span = sub_cat_nav.find('span', {'class': 'img va-product-img'})
                                    final_sub_category_urls = urljoin(parent_url, sub_cats_span.find('a').get('href'))
                                    final_sub_category_name = sub_cats_span.find('img').get('alt')
                                    # final_sub_cate_img = sub_cats_span.find('img').get('src')
                                    # if final_sub_cate_img is not None:
                                    #     sub_cat_img_download_func(final_sub_cate_img,final_sub_category_name.lower().replace("-",'').replace(",",'').replace("/",'').replace("@",''))
                                    # else:
                                    #     print("image not found")
                                    #     pass
                                    print("final_Subcategory: ",p3_id, final_sub_category_name, final_sub_category_urls)
                                    # try:
                                    #     val = (
                                    #         final_sub_category_name, final_sub_category_name, final_sub_category_name,
                                    #         final_sub_category_name.replace(' ', '').replace('-','').replace('/','')+'.jpg', "Yes", "Yes", "Yes", p3_id,
                                    #         final_sub_category_name.replace('-','').replace('/','').replace(' ','').strip(), "Yes")
                                    #     cat_data_insertion(val)
                                    # except Exception as e:
                                    #     print(e)
                                    cat_id = cat_id + 1
                                    try:
                                        categorylist = []
                                        mydb = mysql.connector.connect(
                                            host="localhost",
                                            user="root",
                                            passwd="",
                                            database="uk_electronic"
                                        )
                                        mycursor = mydb.cursor()

                                        sql = "SELECT category_id FROM category WHERE category_name ='%s'" % final_sub_category_name
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
                                            database="uk_electronic"
                                        )
                                        mycursor = mydb.cursor()
                                        sql = "SELECT category_id FROM products"
                                        mycursor.execute(sql)
                                        myresult = mycursor.fetchall()
                                        for x in myresult:
                                            cat_id = x[0]
                                            catelist.append(cat_id)
                                        print(catelist)
                                        for category_id_ in categorylist:
                                            if category_id_ in catelist:
                                                pass
                                                print("Already Exist in Database")
                                            else:
                                                extraction_prod_urls(final_sub_category_urls, category_id_)
                                    except:
                                        pass

                            else:
                                print("No More Subcategories against this url", inner_sub_category_urls)
                        except:
                            pass
                else:
                    print("No More Subcategories against this url",sub_category_urls)
                    pass
    except:
        traceback.print_exc()
        pass
    driver.close()
    driver.quit()

    print("Yahoo Categories End")
    print("Yahoo Categories End")
    print("Yahoo Categories End")
    print("Yahoo Categories End")

#<----------------------------Fetching products_urls------------------------------------->

def extraction_prod_urls(final_sub_category_urls,category_id):
    driver = runfirfoxOverServer()
    parent_url = 'https://www.ukelectricalsupplies.com/'
    url = final_sub_category_urls
    cat_id = category_id
    try:
        driver.get(url)
        time.sleep(1)
        page_scroller(driver,15)
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        Total_Products = page_soup.find('div', {'class': 'ex_title'}).text.strip('products')
        all_product_div = page_soup.find('div', {'class': 'prod_cat_wrapper'})
        product_list_div = all_product_div.find_all('div', {'class': 'fname_text'})
        scrolled_products = len(product_list_div)
        for anchor_urls in product_list_div:
            product_urls = urljoin(parent_url, anchor_urls.find('a').get('href'))
            extraction_product_data(product_urls,cat_id)

    except:
        traceback.print_exc()
        pass
    driver.close()
    driver.quit()
#<----------------------------Fetching products_data------------------------------------->

def extraction_product_data(product_urls , cat_id):
    print(product_urls , cat_id)
    driver = runfirfoxOverServer()
    parent_url = 'https://www.ukelectricalsupplies.com/'
    #<----------------------------------Fetching category id------------------------------------------>
    driver.get(product_urls)
    time.sleep(1)
    try:
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        # <----------------------------Fetching product_title------------------------------------->
        try:
            product_title = page_soup.find('div', {'class': 'prod_heading'}).text.strip()
        except:
            pass

        # <----------------------------Fetching product_code------------------------------------->
        try:
            product_code_div = page_soup.find('div', {'class', 'prod_brandcode'})
            product_code = product_code_div.find('span', {'class', 'proddetail'}).text.strip()
        except:
            pass

        # <----------------------------Fetching product_brand------------------------------------->
        try:
            product_code_div = page_soup.find('div', {'class', 'prod_brandcode'})
            productbrand = product_code_div.find_all('span', {'class', 'proddetail'})[1]
            product_brand = productbrand.text.strip()
        except:
            pass

        # <----------------------------Fetching product_images------------------------------------->
        try:
            product_image_div = page_soup.find('div', {'class': 'main_image_div'})
            single_image = product_image_div.find('a')
            if single_image is not None:
                product_image = single_image.find('img').get('src')
                product_feature_image = product_image
                prod_img_download_func(product_image, product_title.lower().replace("/",'').replace(",",'').replace("-",'').replace("@",'').strip())
            else:
                product_image_div = page_soup.find('div', {'class': 'main_image_div'})
                multiple_images = product_image_div.find_all('img')
                if multiple_images is not None:
                    for i in multiple_images:
                        images = i.get('src')
                        first_image = images[0]
                        print("else images...........")
                        prod_img_download_func(first_image, product_title.lower().replace("/",'').replace(",",'').replace("-",'').replace("@",'').strip())
                else:
                    pass
        except:
            pass

        # <----------------------------Fetching product_old_price------------------------------------->

        try:
            price_div = page_soup.find('div', {'class': 'prod_prices'})
            old_price = price_div.find('div', {'class', 'new_rrp'}).text
        except:
            pass

        # <----------------------------Fetching product_price------------------------------------->

        try:
            price_div = page_soup.find('div', {'class': 'prod_prices'})
            product_price = price_div.find('span', {'class', 'prod_view_price'}).text.replace('£', '').strip()
        except:
            pass

        # <----------------------------Fetching product_description------------------------------------->
        try:
            driver.find_element_by_css_selector(
                '#tabbed-nav > ul.z-tabs-nav.z-tabs-desktop.z-hide-menu > li.z-tab.z-first.z-active').click()
            time.sleep(1)
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            product_detail = page_soup.find('div', {'class', 'z-content-inner'})
            product_description = product_detail.text.strip()
        except:
            pass

        # <----------------------------Database query(products data)------------------------------------->

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="uk_electronic"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO products (product_name,product_description,meta_title,meta_description,meta_keywords,status,category_id,feature_image,IsHome,IsFeature,IsSpecial,product_url,pro_price)" \
                  " VALUES (%s, %s,%s, %s, %s,%s, %s,%s,%s,%s,%s,%s,%s)"
            val = (
                product_title, product_description, product_title,
                product_title, product_title, "Yes", cat_id,
                product_title.lower().replace(',', '').replace('-', '').replace(' ', '').replace('/', '').strip() + '.jpg', 'Yes',
                'Yes', 'Yes', product_title.replace('-', '').replace(',', '').replace('@', '').replace(' ', '').strip(),
                product_price)
            mycursor.execute(sql, val)

            mydb.commit()

            print(mycursor.rowcount, "product inserted.")
            mydb.close()
        except Exception as e:
            print("Product not inserted")
            print(e)

        # <#----------------query to fetch product_id----------------->
        # <----------------------------Database query(fetched products_id)------------------------------------->
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="uk_electronic"
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
        # <----------------------------Database query(products_multiple_images)------------------------------------->

        try:
            thumnail_div = page_soup.find('div', {'aria-label': 'Carousel Pagination'})
            multiple_images = thumnail_div.find_all('span', {'aria-controls': 'product-images-hero'})
            if multiple_images is not None:
                print("Multiple images found")
                z = 0
                for i in multiple_images:
                    images = i.find('img').get('src')
                    multi_prod_img_download_func(images, product_title.lower().replace("/",'').replace(",",'').replace("-",'').replace("@",'').strip(), z)
                    multiple_images = (product_title + str(z) + '.jpg')
                    print(multiple_images)
                    try:
                        mydb = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            passwd="",
                            database="uk_electronic"
                        )
                        mycursor = mydb.cursor()

                        sql = "INSERT INTO products_images (product_id,image_file)" \
                              " VALUES (%s,%s)"
                        val = (product_id,
                               multiple_images.lower().replace(',', '').replace('-', '').replace('/', '').replace('@',
                                                                                                          '').replace(
                                   ' ', '').strip() + '.jpg')
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
            images = '00'
            pass

        # <----------------------------Clicked Varriations (products data)------------------------------------->
        # <----------------------------Clicked Varriations (products data)------------------------------------->
        try:
            dropdown_variations = page_soup.find('select', {'id': 'children_select'})
            if dropdown_variations is not None:
                try:
                    all_variations = dropdown_variations.find_all('option')
                    for values in all_variations:
                        variation_values_ = values.get('value')
                        variation_url = urljoin(parent_url, variation_values_)
                        extractvariationproducts(variation_url, cat_id)

                except Exception as e:
                    print(e)
                    pass
            else:
                pass
        except:
            pass
    except Exception as e:
        print(e)
        pass
    driver.close()
    driver.quit()

def extractvariationproducts(variation_url , cat_id):
    print('Entered in variations_urls')
    driver =runfirfoxOverServer()
    parent_url = 'https://www.ukelectricalsupplies.com/'
    driver.get(variation_url)
    time.sleep(1)
    try:
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # <----------------------------Fetching product_title------------------------------------->
        try:
            product_title = page_soup.find('div', {'class': 'prod_heading'}).text.strip()
        except:
            pass

        # <----------------------------Fetching product_code------------------------------------->
        try:
            product_code_div = page_soup.find('div', {'class', 'prod_brandcode'})
            product_code = product_code_div.find('span', {'class', 'proddetail'}).text.strip()
        except:
            pass

        # <----------------------------Fetching product_brand------------------------------------->
        try:
            product_code_div = page_soup.find('div', {'class', 'prod_brandcode'})
            productbrand = product_code_div.find_all('span', {'class', 'proddetail'})[1]
            product_brand = productbrand.text.strip()
        except:
            pass

        # <----------------------------Fetching product_images------------------------------------->
        try:
            product_image_div = page_soup.find('div', {'class': 'main_image_div'})
            single_image = product_image_div.find('a')
            if single_image is not None:
                product_image = single_image.find('img').get('src')
                prod_img_download_func(product_image, product_title.lower().replace("/",'').replace(",",'').replace("-",'').replace("@",'').strip())
            else:
                product_image_div = page_soup.find('div', {'class': 'main_image_div'})
                multiple_images = product_image_div.find_all('img')
                if multiple_images is not None:
                    for i in multiple_images:
                        images = i.get('src')
                        first_image = images[0]
                        print("else images...........")
                        prod_img_download_func(first_image, product_title.lower().replace("/",'').replace(",",'').replace("-",'').replace("@",'').strip())
                else:
                    pass
        except:
            pass

        # <----------------------------Fetching product_old_price------------------------------------->

        try:
            price_div = page_soup.find('div', {'class': 'prod_prices'})
            old_price = price_div.find('div', {'class', 'new_rrp'}).text
        except:
            pass

        # <----------------------------Fetching product_price------------------------------------->

        try:
            price_div = page_soup.find('div', {'class': 'prod_prices'})
            product_price = price_div.find('span', {'class', 'prod_view_price'}).text.replace('£', '').strip()
        except:
            pass

        # <----------------------------Fetching product_description------------------------------------->
        try:
            driver.find_element_by_css_selector(
                '#tabbed-nav > ul.z-tabs-nav.z-tabs-desktop.z-hide-menu > li.z-tab.z-first.z-active').click()
            time.sleep(1)
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            product_detail = page_soup.find('div', {'class', 'z-content-inner'})
            product_description = product_detail.text.strip()
        except:
            pass

        # <----------------------------Database query(products data)------------------------------------->

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="uk_electronic"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO products (product_name,product_description,meta_title,meta_description,meta_keywords,status,category_id,feature_image,IsHome,IsFeature,IsSpecial,product_url,pro_price)" \
                  " VALUES (%s, %s,%s, %s, %s,%s, %s,%s,%s,%s,%s,%s,%s)"
            val = (
                product_title, product_description, product_title,
                product_title, product_title, "Yes", cat_id,
                product_title.lower().replace(',', '').replace('-', '').replace(' ', '').replace('/', '') + '.jpg', 'Yes',
                'Yes', 'Yes', product_title.replace('-', '').replace(',', '').replace('@', '').replace(' ', '').strip(),
                product_price)
            mycursor.execute(sql, val)

            mydb.commit()
            print('product inserted')
            print(mycursor.rowcount, "product inserted.")
            mydb.close()
        except Exception as e:
            print("Product not inserted")
            print(e)

        # <----------------------------Database query(fetched products_id)------------------------------------->
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="uk_electronic"
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
        # <----------------------------Database query(products_multiple_images)------------------------------------->

        try:
            thumnail_div = page_soup.find('div', {'aria-label': 'Carousel Pagination'})
            multiple_images = thumnail_div.find_all('span', {'aria-controls': 'product-images-hero'})
            if multiple_images is not None:

                # <----------------------------Database query(fetched products_id)------------------------------------->
                z = 0
                for i in multiple_images:
                    images = i.find('img').get('src')
                    multi_prod_img_download_func(images, product_title.lower().replace("/",'').replace(",",'').replace("-",'').replace("@",'').strip(), z)
                    multiple_images = (product_title.lower().replace("/",'').replace(",",'').replace("-",'').replace("@",'').strip() + str(z) + '.jpg')
                    print(multiple_images)
                    try:
                        mydb = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            passwd="",
                            database="uk_electronic"
                        )

                        mycursor = mydb.cursor()

                        sql = "INSERT INTO products_images (product_id,image_file)" \
                              " VALUES (%s,%s)"
                        val = (product_id,
                               multiple_images.lower().replace(',', '').replace('-', '').replace('/', '').replace('@',
                                                                                                          '').replace(
                                   ' ', '') + '.jpg')
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
            images = '00'
            pass
    except Exception as e:
        print(e)
        pass
    driver.close()
    driver.quit()


if __name__ == '__main__':
    fetching_main_cats()
