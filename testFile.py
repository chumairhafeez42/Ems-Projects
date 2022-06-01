# import codecs
#
# scraped_write = codecs.open("scraped_file.txt", "a")
# for file in range(5):
#     scraped_write.write("file" + "\n")
# import pdfkit
#
# options = {
#     'page-size': 'Letter',
#     'margin-top': '0.0in',
#     'margin-right': '0.0in',
#     'margin-bottom': '0.0in',
#     'margin-left': '0.0in'}
# pdfkit.from_file(f'/home/amir/PycharmProjects/google-selenium/enwiki-20220301-pages-meta-history2_html/Tikander Lake, Minnesota.html',
#                  f'/home/amir/PycharmProjects/google-selenium/pdf/Tikander Lake, Minnesota.pdf', options=options)
# import os
# import re
# from pathlib import Path
#
# parent_path = '/home/amir/Desktop/Unused Data/enwiki-20220301-pages-articles-multistream2_html'
# filenames = next(
#     os.walk((parent_path)), (None, None, []))[2]
# print(len(filenames))
# count = 1
# i = 1
# new_list = []
# for file in (filenames):
#     with open(parent_path + "/" + file, "r+") as f:
#         text = f.read()
#         if "image_link" in text:
#             # print(i,"'"+file+"',")
#             # i += 1
#             new_list.append(file)
# print(len(new_list))

# import re
#
# string = '<img src=https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5t_JKlO_W8VjkAvmJOvTUDfZwwAJ9Ry9QmSG8OJXZpB098JD1-CGcFryWq2A&s alt="Thumbnail" style="height: 300px; width: 300px; object-fit: contain;"/>'
# ip_regex = re.search(r"(?<=src=)(.*)(?= alt=)", string).group(1)
# print(ip_regex)

import datetime
import json
import os
import time
import traceback
from multiprocessing.pool import ThreadPool

from tinydb import table, TinyDB, where
from textspitter import TextSpitter
# from config.utils import get_current_time, compress_text
import string
import uuid


def get_text_save_words(filename):
    full_text = ''
    extension = filename.rsplit('.')[-1].lower()
    try:
        if extension in ("pdf", "docx", "txt", "text"):
            full_text = TextSpitter(filename=filename)
    except Exception as error:
        pass
    return full_text


def insert_db(items):
    db = TinyDB("testing123.json")
    for item in items:
        item = json.loads(item)
        print(item)
        try:
            db.upsert(table.Document(item["content"], doc_id=uuid.uuid4().int & (1 << 64) - 1),
                      where('filepath') == item["filepath"])
        except:
            traceback.print_exc()
            print(item[0])
            time.sleep(10000)


def PoolCode(func, sublink, pool_number):
    chunksList = []
    for i in range(0, len(sublink), 20):
        chunk = sublink[i: i + 20]
        chunksList.append(chunk)
    pool_size = pool_number
    pool = ThreadPool(pool_size)
    pool.map(func, chunksList)
    pool.close()
    pool.join()
    print('done pooling')
    print('Done Product Pool')


if __name__ == '__main__':

    folder_path = "/home/amir/Desktop/Complete Scraped Data PDF/enwiki-20220301-pages-articles-multistream1"
    # filename = "/home/amir/Desktop/Complete Scraped Data
    # PDF/enwiki-20220301-pages-articles-multistream1/Conjunction introduction.pdf"
    filenames = next(os.walk(folder_path), (None, None, []))[2]
    filenames = filenames[0:5]

    db_list = []
    for file in filenames:
        start_time = datetime.datetime.now()
        file_path = folder_path + "/" + file
        full_text = get_text_save_words(file_path)
        end_time = datetime.datetime.now()
        elapsed_seconds = (end_time - start_time).seconds

        item = {"content": str(full_text), "filepath": file_path}
        data = json.dumps(item)
        db_list.append(data)
        if len(db_list) >= 4:
            db_start_time = datetime.datetime.now()
            PoolCode(insert_db, db_list, 1)
            db_list.clear()
            db_end_time = datetime.datetime.now()
            db_elapsed_seconds = (db_end_time - db_start_time).seconds
            print("Db insertion Time", db_elapsed_seconds)
        # db.upsert(item, where('filepath') == file_path)

        print("conversion Time", elapsed_seconds)


