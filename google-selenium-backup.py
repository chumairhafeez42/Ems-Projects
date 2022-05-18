import codecs
import logging
import os
import random
import re
import time
import traceback
from multiprocessing.pool import ThreadPool
from pathlib import Path

import pdfkit as pdfkit
import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename="app.log", filemode="w")


def run_chrome_over_server():
    while True:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--shm-size=2g")
            options.add_argument("--no-sandbox")
            options.add_argument("--remote-debugging-port=9222")
            while True:
                try:
                    driver = webdriver.Chrome(
                        service=Service(ChromeDriverManager().install()),
                        options=options,
                    )
                except:
                    driver = webdriver.Chrome(
                        executable_path="/chromedriver76", options=options
                    )
                break
            print("driver created")
            return driver
        except:
            logging.error(str(traceback.print_exc()))


def remove_extra_selenium_tabs(driver):
    driver_len = len(driver.window_handles)  # fetching the Number of Opened tabs
    if driver_len > 1:  # Will execute if more than 1 tabs found.
        for i in range(driver_len - 1, 0, -1):
            driver.switch_to.window(
                driver.window_handles[i]
            )  # will close the last tab first.
            driver.close()
        # Switching the driver focus to First tab.
        driver.switch_to.window(driver.window_handles[0])


def google_selenium_html(queries):
    driver = run_chrome_over_server()
    driver.maximize_window()
    for query in queries:
        if ".html" not in query:
            continue
        if query not in scraped_list:
            try:
                global count
                print(count, query)
                logging.info(count, query)
                count += 1
                search_query = query.replace(".html", "")
                link = (
                    f"https://www.google.com.pk/search?q={search_query}&"
                    f"tbm=isch&hl=en&tbs=il:ol&authuser=0&sa=X&biw=1833&bih=948 "
                )
                driver.get(link)
                time.sleep(random.randint(3, 10))
                div_id = random.randint(1, 4)
                driver.find_element(
                    by=By.XPATH, value=f'//*[@id="islrg"]/div[1]/div[{div_id}]/a[1]'
                ).click()
                time.sleep(random.randint(3, 10))
                remove_extra_selenium_tabs(driver)
                action_chains = ActionChains(driver)
                try:
                    action_chains.context_click(
                        driver.find_element(
                            by=By.XPATH, value='//*[@class="qdnLaf isv-id"]'
                        )
                    ).perform()
                except:
                    action_chains.context_click(
                        driver.find_element(
                            By.XPATH,
                            value='//*[@id="Sva75c"]/div/div/div[3]/div['
                            "2]/c-wiz/div/div[1]/div[1]/div["
                            "3]/div/a",
                        )
                    ).perform()
                remove_extra_selenium_tabs(driver)
                time.sleep(random.randint(1, 4))
                pyautogui.typewrite(
                    [
                        "down",
                        "down",
                        "down",
                        "down",
                        "down",
                        "down",
                        "down",
                        "down",
                        "down",
                        "down",
                        "enter",
                    ]
                )
                image_link = pyperclip.paste()
                logging.info("image_link", image_link)
                with open(os.path.join(complete_folder_path, query), "r+") as file:
                    text = file.read()
                    text = re.sub("image_link", image_link, text)
                    file.seek(0)
                    file.write(text)
                    file.truncate()
                scraped_list.append(query)
                scraped_write.write(query + "\n")
            except:
                traceback.print_exc()
                print("exception", query)
                continue
    driver.quit()


def html_to_pdf(files):
    options = {
        "page-size": "Letter",
        "margin-top": "0.0in",
        "margin-right": "0.0in",
        "margin-bottom": "0.0in",
        "margin-left": "0.0in",
    }
    for html_file in files:
        if ".pdf" in html_file:
            continue
        try:
            updated_file = html_file.replace(".html", "")
            pdfkit.from_file(
                f"{complete_folder_path}/{html_file}",
                f"{parent_path}/pdf/{updated_file}.pdf",
                options=options,
            )
        except:
            print(html_file)
            traceback.print_exc()


def pool_code(func, sub_link, pool_number):
    chunks_list = []
    for i in range(0, len(sub_link), 20):
        chunk = sub_link[i : i + 20]
        chunks_list.append(chunk)
    pool_size = pool_number
    pool = ThreadPool(pool_size)
    pool.map(func, chunks_list)
    pool.close()
    pool.join()
    print("done pooling")


if __name__ == "__main__":
    scraped_read = codecs.open("scraped_file.txt", "r+")
    scraped_write = codecs.open("scraped_file.txt", "a")
    scraped_files = scraped_read.read()
    scraped_list = []
    # ZIP_FILE_PATH = os.getenv('ZIP_FILE_PATH')
    # if ZIP_FILE_PATH:
    #     filename = ZIP_FILE_PATH
    # else:
    #     filename = 'enwiki-20220301-pages-meta-history16.xml-p20567244p20570392.bz2'
    # output_file_name = "-".join(filename.split("-")).split(".")[0].split("/")[-1]
    # text_file_path = f"{output_file_name}_html"
    # parent_path = Path(text_file_path).parent.absolute()
    # filenames = next(
    #     os.walk(os.path.join(parent_path, text_file_path)), (None, None, [])
    # )[2]
    for file in scraped_files.split("\n"):
        if file:
            scraped_list.append(file.strip())
    try:
        folder_path = "enwiki-20220301-pages-meta-history2_html"
        parent_path = Path(folder_path).parent.absolute()
        complete_folder_path = os.path.join(parent_path, folder_path)
        count = 1
        filenames = next(
            os.walk(os.path.join(parent_path, folder_path)), (None, None, [])
        )[2]
        # filenames = filenames[150:170]
        logging.info(len(filenames))
        pool_code(google_selenium_html, filenames, 1)
        pool_code(html_to_pdf, filenames, 2)
    except:
        logging.error(str(traceback.print_exc()))
