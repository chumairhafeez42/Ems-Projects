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
    # driver.get("https://www.theworkplacedepot.co.uk/expanding-belt-barrier")
    # driver.get("https://www.theworkplacedepot.co.uk/outdoor-twin-belt-barrier-yellow-post")
    # driver.get("https://www.theworkplacedepot.co.uk/standard-heavy-duty-pallet-truck")
    # driver.get("https://www.theworkplacedepot.co.uk/column-protector")
    # driver.get("https://www.theworkplacedepot.co.uk/magnetic-selfadhesive-aisle-markers")
    # driver.get("https://www.theworkplacedepot.co.uk/louvred-panel-rack")
    # driver.get("https://www.theworkplacedepot.co.uk/cantilever-racking")
    # driver.get("https://www.theworkplacedepot.co.uk/double-vertical-storage-racking")

    driver , display= runChromeOverServer()
    driver.execute_script("window.open('about:blank','tab1')")
    driver.switch_to.window("tab1")
    driver.get("https://www.theworkplacedepot.co.uk/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "primary-nav")))
    main_cat_ul = driver.find_element_by_id("primary-nav").find_elements_by_css_selector(".section")
    for atag in main_cat_ul:
        main_cat_links = atag.find_element_by_tag_name("a").get_attribute("href")
        main_cat_name = atag.find_element_by_tag_name("a").text
        print(main_cat_name , main_cat_links)
        Sub_cat_ul = atag.find_element_by_css_selector(".dropdown-menu").find_elements_by_tag_name("a")
        for ancho_tag in Sub_cat_ul:
            sub_cat_name = ancho_tag.get_attribute('innerHTML')
            sub_cat_url = ancho_tag.get_attribute("href")
            print(sub_cat_name , sub_cat_url)



    driver.quit()
    # data_ = 10
    # data_ += 1
    # driver.switch_to_window("tab1")

def product_url():
    driver, display = runChromeOverServer()
    driver.execute_script("window.open('about:blank','tab1')")
    driver.switch_to.window("tab1")
    driver.get("https://www.theworkplacedepot.co.uk/pallet-trucks")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "category-tiles")))
    product_url_div = driver.find_element_by_id("category-tiles").find_elements_by_css_selector(".tile-products")
    for link in product_url_div:
        product_url = link.find_element_by_tag_name("a").get_attribute("href")
        print("product_url:" ,product_url)


def product_data():
    parent_url = "https://www.theworkplacedepot.co.uk/"
    driver , display = runChromeOverServer()
    driver.execute_script("window.open('about:blank','tab1')")
    driver.switch_to.window("tab1")
    # driver.get("https://www.theworkplacedepot.co.uk/louvred-panel-rack")
    driver.get("https://www.theworkplacedepot.co.uk/outdoor-twin-belt-barrier-yellow-post")
    # driver.get("https://www.theworkplacedepot.co.uk/expanding-belt-barrier")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "title")))

    # try:
    #     product_title_ = driver.find_element_by_id("title")
    #     product_title = product_title_.text
    #     print(product_title)
    # except:
    #     traceback.print_exc()
    #
    # try:
    #     price_div = driver.find_element_by_css_selector(".price-ex-vat")
    #     product_price = price_div.text.replace("Ex. VAT", "").replace("£","")
    #     print(product_price)
    # except:
    #     traceback.print_exc()
    #
    # try:
    #     features_div = driver.find_element_by_css_selector(".tab-content")
    #     features = features_div.text
    # except:
    #     traceback.print_exc()
    #
    # try:
    #     description_div = driver.find_element_by_xpath("//*[@id='tabbed']/li[2]/a").click()
    #     description_tag = driver.find_element_by_id("specifications")
    #     description_ = description_tag.text
    #     if features is not None:
    #         description = (features +"\n"+ description_)
    #         print("IF Tag" , description)
    #     else:
    #         description = description_
    #         print("Else Tag" , description)
    #
    # except:
    #     traceback.print_exc()
    #
    #
    # try:
    #     image_div = driver.find_element_by_id("extra-img")
    #     image_tags = image_div.find_elements_by_tag_name("img")
    #     for atag in image_tags:
    #         product_images = urljoin(parent_url , atag.get_attribute("data-lg"))
    #         print(product_images)
    # except:
    #     traceback.print_exc()
    #
    # try:
    #     acessories_div = driver.find_element_by_id("accessories")
    #     side_variation_tags = acessories_div.find_elements_by_tag_name("tr")[1:]
    #     for variation_tags in side_variation_tags:
    #         variation_code = variation_tags.find_elements_by_tag_name("td")[0].text
    #         variation_title = variation_tags.find_elements_by_tag_name("td")[1].text
    #         variation_price = variation_tags.find_elements_by_tag_name("td")[2].text
    #         variation = (variation_code +"-"+ variation_title +"-"+ variation_price)
    #         print(variation)
    # except:
    #     pass

    # try:
    #     # clicked = driver.find_element_by_id("chooser-1").click()
    #     driver.find_element_by_xpath("//*[@id='chooser-1']/button").click()
    #     # print("clicked")
    #     # print("clicked")
    #     # time.sleep(2)
    #     first_variation_div = driver.find_element_by_xpath("//*[@id='chooser-1']/ul")
    #     print("clicked")
    #     first_variation_tag = first_variation_div.find_elements_by_tag_name("a")
    #     driver.implicitly_wait(4)
    #     time.sleep(2)
    #     for option in first_variation_tag:
    #         # option.click()
    #         time.sleep(2)
    #         first_variation = option.text
    #         try:
    #             price_div = driver.find_element_by_css_selector(".price-ex-vat")
    #             product_price = price_div.text.replace("Ex. VAT", "").replace("£", "")
    #         except:
    #             traceback.print_exc()
    #         print(first_variation + product_price)
    # except:
    #     traceback.print_exc()

    # try:
    #     #     print("Entered in 2nd variation")
    #     #     driver.find_element_by_id("chooser-1").click()
    #     #     print("clicked")
    #     #     buttons = driver.find_element_by_xpath("//*[@id='chooser-1']/ul")
    #     #     button_li = buttons.find_elements_by_tag_name("li")[1:]
    #     #     driver.implicitly_wait(5)
    #     #     for button in button_li:
    #     #         button.click()
    #     #         print(button.text)
    #     #         # ActionChains(driver).click().perform()
    #     #         try:
    #     #             price_div = driver.find_element_by_css_selector(".price-ex-vat")
    #     #             product_price = price_div.text.replace("Ex. VAT", "").replace("£", "")
    #     #             print(product_price)
    #     #         except:
    #     #             traceback.print_exc()
    #     #             time.sleep(1)
    #     # except:
    #     #     traceback.print_exc()


    try:
        driver.find_element_by_id("chooser-1").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='chooser-1']/ul")))
        first_div = driver.find_element_by_xpath("//*[@id='chooser-1']/ul")
        time.sleep(1)
        first_tag = first_div.find_elements_by_tag_name("a")[1:]
        for atag in first_tag:
            atag.click()
            time.sleep(5)
            print(atag.text)
            print("clicked")
            try:
                price_div = driver.find_element_by_css_selector(".price-ex-vat")
                product_price = price_div.text.replace("Ex. VAT", "").replace("£", "")
                print(product_price)
            except:
                traceback.print_exc()
    except:
        traceback.print_exc()


if __name__ == '__main__':
    # fetching_categories()
    # product_url()
    product_data()
