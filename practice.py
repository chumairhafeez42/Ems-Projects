import time
import traceback

import mysql.connector
from selenium import webdriver

from strictly_table_chair.absolute_tablechair import multi_prod_img_download_func, prod_img_download_func
from ukelectric.uk_all_function import exceptionMessage
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time

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

def varriations():
    driver = runfirfoxOverServer()
    # driver = webdriver.Chrome(executable_path=r"E:\Emsgroup\web_driver\chromedriver.exe")
    data_ = 5
    cat_id = 1
    try:
        driver.execute_script("window.open('about:blank','tab" + str(data_) + "')")
        driver.switch_to.window("tab" + str(data_))
        driver.get("https://www.strictlytablesandchairs.co.uk/easycare-napkin-plain-20-x-20-51cm-x-51cm/")
        # print(pro_url)
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
            sql = "SELECT product_id FROM products WHERE product_name  ='%s'" % product_title
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            for x in myresult:
                product_id = x[0]
            print('product_id is : ', product_id)
            mydb.close()
        except:
            pass

        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-custom-option")))
            color_variation_div = driver.find_element_by_css_selector(".product-custom-option")
            size_id = 1
            if color_variation_div:
                print("Entered in variations")
                options = color_variation_div.find_elements_by_tag_name("option")[1:]
                for option in options:
                    fabric_color = option.text.strip()
                    price_tag = "£"
                    if price_tag in fabric_color:
                        option.click()
                        try:
                            price_div = driver.find_elements_by_css_selector(".price-excluding-tax")
                            for price_ in price_div:
                                product_price = price_.text.replace('£', '').strip()
                                print(product_price)
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
                                    val = (size_id, product_id, product_price,fabric_color)
                                    mycursor.execute(sql, val)
                                    mydb.commit()
                                    print(mycursor.rowcount, "size_product inserted.")
                                    mydb.close()
                                except Exception as e:
                                    traceback.print_exc()
                                    print(e)
                                    pass
                                size_id += 1
                        except Exception as e:
                            traceback.print_exc()
                            print(e)
                    else:
                        try:
                            price_div = driver.find_elements_by_css_selector(".price-excluding-tax")
                            for price_ in price_div:
                                product_price = price_.text.replace('£', '').strip()
                                print(product_price)
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
                                    val = (size_id, product_id, product_price,fabric_color)
                                    mycursor.execute(sql, val)
                                    mydb.commit()
                                    print(mycursor.rowcount, "size_product inserted.")
                                    mydb.close()
                                except Exception as e:
                                    traceback.print_exc()
                                    print(e)
                                    pass
                                size_id += 1
                        except Exception as e:
                            print(e)
            else:
                pass
        except:
            pass
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ox-picker")))
            variation_div = driver.find_element_by_css_selector('.ox-picker')
            if variation_div is not None:
                variation_tags = variation_div.find_elements_by_tag_name('img')
                for atags in variation_tags:
                    image_tags = atags.get_attribute('src')
                    pro_images = image_tags.split('/')[-1]
                    fabric_color = pro_images.replace('.png', '').replace('.jpeg', '').replace('.jpg', '')
                    print(fabric_color)
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
                        val = (size_id, product_id, product_price, fabric_color)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        print(mycursor.rowcount, "size_product inserted.")
                        mydb.close()
                    except Exception as e:
                        traceback.print_exc()
                        print(e)
                        pass
                    size_id += 1
            else:
                pass
        except:
            pass
    except:
        traceback.print_exc()
    data_ += 1
    driver.quit()

def query2():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="tablechair"
        )
        mycursor = mydb.cursor()
        sql = "DELETE FROM products_size WHERE price = '0'"
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")
    except:
        pass

def tablechair():
    driver , display = runChromeOverServer()
    # driver.get("https://www.strictlytablesandchairs.co.uk/easycare-napkin-plain-20-x-20-51cm-x-51cm/")
    # driver.get("https://www.strictlytablesandchairs.co.uk/chiavari-chair-stacking-chairs-white-frame-im/")
    # driver.get("https://www.strictlytablesandchairs.co.uk/bendi-aluminium-stacking-chair-v19/")
    # driver.get("https://www.strictlytablesandchairs.co.uk/steel-stacking-chair-premium-600a-ser/")
    # driver.get("https://www.strictlytablesandchairs.co.uk/chiavari-chair-stacking-chairs-gold-frame/")
    # driver.get("https://www.strictlytablesandchairs.co.uk/semicircle-lightweight-aluminium-folding-table-150cm/")
    # driver.get("https://www.strictlytablesandchairs.co.uk/lightweight-aluminium-conference-board-room-tables/")
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-custom-option")))
        color_variation_div = driver.find_element_by_css_selector(".product-custom-option")
        if color_variation_div:
            options = color_variation_div.find_elements_by_tag_name("option")[1:]
            for option in options:
                fabric_color = option.text.strip()
                price_tag = "£"
                if price_tag in fabric_color:
                    option.click()
                    try:
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ox-picker")))
                        variation_div = driver.find_element_by_css_selector('.ox-picker')
                        if variation_div is not None:
                            print("Entered in Varriation Div")
                            variation_tags = variation_div.find_elements_by_tag_name('img')
                            for atags in variation_tags:
                                image_tags = atags.get_attribute('src')
                                pro_images = image_tags.split('/')[-1]
                                colors = pro_images.replace('.png', '').replace('.jpeg', '').replace('.jpg', '')
                                print(colors)
                        else:
                            pass
                    except:
                        price_div = driver.find_elements_by_css_selector(".price-excluding-tax")
                        for price_ in price_div:
                            price = price_.text.replace('£', '').strip()
                            print(price)
                else:
                    print(fabric_color)
        else:
            pass
    except:
        traceback.print_exc()
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ox-picker")))
        variation_div = driver.find_element_by_css_selector('.ox-picker')
        if variation_div is not None:
            print("Entered in Varriation Div")
            variation_tags = variation_div.find_elements_by_tag_name('img')
            for atags in variation_tags:
                image_tags = atags.get_attribute('src')
                pro_images = image_tags.split('/')[-1]
                colors = pro_images.replace('.png','').replace('.jpeg','').replace('.jpg','')
                print(colors)
        else:
            pass
    except:
        pass





def variations_tags():
    driver, display = runChromeOverServer()
    # driver.get("https://www.strictlytablesandchairs.co.uk/easycare-napkin-plain-20-x-20-51cm-x-51cm/")
    # driver.get("https://www.strictlytablesandchairs.co.uk/chiavari-chair-stacking-chairs-white-frame-im/")
    # driver.get("https://www.strictlytablesandchairs.co.uk/bendi-aluminium-stacking-chair-v19/")
    # driver.get("https://www.strictlytablesandchairs.co.uk/steel-stacking-chair-premium-600a-ser/")
    # driver.get("https://www.strictlytablesandchairs.co.uk/chiavari-chair-stacking-chairs-gold-frame/")
    # driver.get("https://www.strictlytablesandchairs.co.uk/semicircle-lightweight-aluminium-folding-table-150cm/")
    driver.get("https://www.strictlytablesandchairs.co.uk/lightweight-aluminium-conference-board-room-tables/")
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
                if price is not None:
                    print(fabric_color+"-"+ price)
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
                        val = (size_id, product_id, product_price, fabric_color)
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
                                if price is not None:
                                    print(fabric_color +" "+ fabric_color_ + "-" + price)
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
                                        val = (size_id, product_id, product_price, fabric_color)
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
                    if price is not None:
                        print(fabric_color_ + "-" + price)
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
                            val = (size_id, product_id, product_price, fabric_color)
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




if __name__ == '__main__':
    # tablechair()
    # varriations()
    # query2()
    variations_tags()



