import codecs
import os
import random
import re
import time
import traceback
from pathlib import Path
import requests
from bs4 import BeautifulSoup

from text_parser_html import pool_code


def google_request(queries):
    for query in queries:
        try:
            if ".txt" in query:
                query = query.replace(".txt", "")
            link = f"https://www.bing.com/images/search?sp=-1&sc=0-0&cvid=D88F006A9B0B4194BD401B5FE0F77AD8&q=burger&qft=+filterui:license-L2_L3_L4_L5_L6_L7&form=IRFLTR&first=1&tsc=ImageHoverTitle"
            r = requests.get(link)
            wait = random.randint(1, 2)
            time.sleep(wait)
            soup = BeautifulSoup(r.text, "html.parser")
            main_div = soup.find("div", {"class": "lIMUZd"})
            image_link = main_div.find("img")['src']
            print(image_link)
            with open(os.path.join(complete_folder_path, query), "r+") as file:
                text = file.read()
                text = re.sub("image_link", image_link, text)
                file.seek(0)
                file.write(text)
                file.truncate()
            scraped_list.append(query)
            scraped_write.write(query + "\n")
        except:
            print("exception1", query)
            with open(os.path.join(complete_folder_path, query), "r+") as file:
                text = file.read()
                text = re.sub("image_link",
                              "https://image.shutterstock.com/image-photo/scenery-green-golf-meadow-sunbeam-260nw-1210369285.jpg",
                              text)
                file.seek(0)
                file.write(text)
                file.truncate()
            scraped_list.append(query)
            scraped_write.write(query + "\n")
            continue


if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/86.0.4240.75 Safari/537.36'}

    scraped_read = codecs.open("scraped_file_requests.txt", "r+")
    scraped_write = codecs.open("scraped_file_requests.txt", "a")
    scraped_files = scraped_read.read()
    scraped_list = []
    ZIP_FILE_PATH = os.getenv('ZIP_FILE_PATH')
    if ZIP_FILE_PATH:
        filename = ZIP_FILE_PATH
    else:
        filename = 'enwiki-20220301-pages-meta-history16.xml-p20567244p20570392.bz2'
    for file in scraped_files.split("\n"):
        if file:
            scraped_list.append(file.strip())
    try:
        folder_name = "-".join(filename.split("-")).split(".")[0].split("/")[-1]
        print(folder_name)
        # folder_path = f"{folder_name}_html"
        if "html" in folder_name:
            folder_path = f"{folder_name}"
        else:
            folder_path = f"{folder_name}_html"
        parent_path = Path(folder_path).parent.absolute()
        complete_folder_path = os.path.join(parent_path, folder_path)
        filenames = next(
            os.walk(os.path.join(parent_path, folder_path)), (None, None, [])
        )[2]
        count = 1
        filenames = filenames[:100]
        print(len(filenames))
        for file in filenames:
            if file in scraped_list:
                filenames.remove(file)
        print(len(filenames))
        pool_code(google_request, filenames, 2)
        # pool_code(html_to_pdf, filenames, 2)
        scraped_read.close()
        scraped_write.close()
    except:
        traceback.print_exc()

    # google_request(['burger'])