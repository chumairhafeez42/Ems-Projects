import traceback
from multiprocessing.pool import ThreadPool

import requests
import urllib.request
import os
import re
from pathlib import Path

def download_images(image_list):
    global index
    for image in (image_list):
        try:
            index += 1
            print(index, image[0])
            urllib.request.urlretrieve(image[1], f"{destination_folder}/{image[0]}.jpg")
        except:
            print(image)
            continue
        # img_data = requests.get(image[1]).content
        # with open(f'{destination_folder}/{image[0]}.jpg', 'wb') as handler:
        #     handler.write(img_data)

def get_image_urls(filenames):
    image_list = []
    for file in (filenames):
        try:
            with open(parent_path + "/" + file, "r+") as f:
                text = f.read()
                ip_regex = re.search(r"(?<=src=)(.*)(?= alt=)", text).group(1)
                image_list.append((file.replace(".html", ""), ip_regex))
        except:
            print(text)
            continue
    return image_list


def remove_files(files):
    for html_file in files:
        global index
        print(index, html_file)
        index += 1
        if ".pdf" in html_file:
            continue
        try:
            updated_file = html_file.replace(".html", "")
            # print(f"{destination_folder}/{updated_file}.jpg")
            os.remove(f"{destination_folder}/{updated_file}.jpg")
        except:
            traceback.print_exc()


def pool_code(func, sub_link, pool_number):
    chunks_list = []
    for i in range(0, len(sub_link), 5):
        chunk = sub_link[i : i + 5]
        chunks_list.append(chunk)
    pool_size = pool_number
    pool = ThreadPool(pool_size)
    pool.map(func, chunks_list)
    pool.close()
    pool.join()
    print("done pooling")


if __name__ == '__main__':
    destination_folder = "/home/amir/Desktop/Requests-Images/enwiki-20220301-pages-meta-history7_html"
    parent_path = '/home/amir/Desktop/Complete Scraped Data 18-05-2022/enwiki-20220301-pages-meta-history7_html'
    # destination_folder = "/home/amir/Desktop/Only PDFs/enwiki-20220301-pages-articles-multistream11_1_html"
    # parent_path = '/home/amir/Desktop/Unused Data/enwiki-20220301-pages-articles-multistream11_1_html'
    filenames = next(
        os.walk((parent_path)), (None, None, []))[2]
    # print(len(filenames))
    index = 0
    image_list = []
    # filenames = filenames[10500:11000]
    filenames = filenames[2000:]
    # images = [('Computable number', 'https://mindmatters.ai/wp-content/uploads/sites/2/2021/04/list-of-prime-numbers-below-100-vintage-type-writer-from-1920s-stockpack-adobe-stock-1597x1597.jpg'),
    #              ('Benfords law', 'https://www.embryodigital.co.uk/wp-content/uploads/2021/09/shutterstock_126304538-scaled-e1637072735455.jpg')]
    images = get_image_urls(filenames)
    pool_code(download_images, images, 3)
    # remove_files(filenames)