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
import io
import json
import os
import time
import traceback
import urllib
from multiprocessing.pool import ThreadPool

import requests
from tinydb import table, TinyDB, where
# from textspitter import TextSpitter
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

def process_docs(item, db):
    remove_keys = ('filepath', 'parent', 'folder', '_sa_instance_state')
    content = item['content']
    if len(content) > 200:
        ipfs_hash = "aqwsdefrgthyjuok"
        item['content'] = ''
        item['content_hash'] = ipfs_hash
    item = {key: item[key] for key in item.keys() if key not in remove_keys}
    return item


if __name__ == '__main__':

    # folder_path = "/home/amir/Desktop/Complete Scraped Data PDF/enwiki-20220301-pages-articles-multistream1"
    # # filename = "/home/amir/Desktop/Complete Scraped Data
    # # PDF/enwiki-20220301-pages-articles-multistream1/Conjunction introduction.pdf"
    # filenames = next(os.walk(folder_path), (None, None, []))[2]
    # filenames = filenames[0:5]
    #
    # db_list = []
    # for file in filenames:
    #     start_time = datetime.datetime.now()
    #     file_path = folder_path + "/" + file
    #     full_text = get_text_save_words(file_path)
    #     end_time = datetime.datetime.now()
    #     elapsed_seconds = (end_time - start_time).seconds
    #
    #     item = {"content": str(full_text), "filepath": file_path}
    #     data = json.dumps(item)
    #     db_list.append(data)
    #     if len(db_list) >= 4:
    #         db_start_time = datetime.datetime.now()
    #         PoolCode(insert_db, db_list, 1)
    #         db_list.clear()
    #         db_end_time = datetime.datetime.now()
    #         db_elapsed_seconds = (db_end_time - db_start_time).seconds
    #         print("Db insertion Time", db_elapsed_seconds)
    #     # db.upsert(item, where('filepath') == file_path)
    #
    #     print("conversion Time", elapsed_seconds)

    # docs = [{'_sa_instance_state': '<sqlalchemy.orm.state.InstanceState object at 0x7f1bf037dfd0>', 'status': 1, 'parent': '/home/amir/Desktop/Fruits', 'size': '155.34 KB', 'modified_at': 1649936108, 'extension': 'jpg', 'filepath': '/home/amir/Desktop/Fruits/Do_Apples_Affect_Diabetes_and_Blood_Sugar_Levels-732x549-thumbnail-1-732x549.jpg', 'ipfs_hash': 'QmPUgSEYrgFF3DLDJMFtfPWmm3yQFe5HQXEGP25G3sAKkd', 'size_in_bytes': 159070, 'id': 1, 'created_at': 1655707147.2161052, 'name': 'Do_Apples_Affect_Diabetes_and_Blood_Sugar_Levels-732x549-thumbnail-1-732x549', 'folder': '/home/amir/Desktop/Fruits', 'content': 'apple donut sports ball'},
    #         {'_sa_instance_state': '<sqlalchemy.orm.state.InstanceState object at 0x7f1bf037dfa0>', 'status': 1, 'parent': '/home/amir/Desktop/Fruits', 'size': '3.17 KB', 'modified_at': 1648808365, 'extension': 'jpeg', 'filepath': '/home/amir/Desktop/Fruits/images.jpeg', 'ipfs_hash': 'QmPUgSEYrgFF3DLDJMFtfPWmm3yQFe5HQXEGP25G3sAKkd', 'size_in_bytes': 3246, 'id': 2, 'created_at': 1655707147.2081053, 'name': 'images', 'folder': '/home/amir/Desktop/Fruits', 'content': 'banana scissors'},
    #         {'_sa_instance_state': "<sqlalchemy.orm.state.InstanceState object at 0x7f1bf037dee0>", 'status': 1, 'parent': '/home/amir/Desktop/Fruits', 'size': '174.33 KB', 'modified_at': 1648808319, 'extension': 'jpg', 'filepath': '/home/amir/Desktop/Fruits/apple-fruit.jpg', 'ipfs_hash': 'QmPUgSEYrgFF3DLDJMFtfPWmm3yQFe5HQXEGP25G3sAKkd', 'size_in_bytes': 178517, 'id': 3, 'created_at': 1655707147.2081053, 'name': 'apple-fruit', 'folder': '/home/amir/Desktop/Fruits', 'content': 'vase apple'},
    #         {'_sa_instance_state': '<sqlalchemy.orm.state.InstanceState object at 0x7f1bf037de80>', 'status': 1, 'parent': '/home/amir/Desktop/Fruits', 'size': '140.37 KB', 'modified_at': 1649932812, 'extension': 'jpg', 'filepath': '/home/amir/Desktop/Fruits/kawaii-cute-happy-pineapple-vegetable-vector-14292000.jpg', 'ipfs_hash': 'QmPUgSEYrgFF3DLDJMFtfPWmm3yQFe5HQXEGP25G3sAKkd', 'size_in_bytes': 143736, 'id': 4, 'created_at': 1655707147.2161052, 'name': 'kawaii-cute-happy-pineapple-vegetable-vector-14292000', 'folder': '/home/amir/Desktop/Fruits', 'content': ''},
    #         {'_sa_instance_state': '<sqlalchemy.orm.state.InstanceState object at 0x7f1bf037dbb0>', 'status': 1, 'parent': '/home/amir/Desktop/Fruits', 'size': '5.51 KB', 'modified_at': 1649936198, 'extension': 'jpg', 'filepath': '/home/amir/Desktop/Fruits/1566389294_04414_pic.jpg', 'ipfs_hash': 'QmPUgSEYrgFF3DLDJMFtfPWmm3yQFe5HQXEGP25G3sAKkd', 'size_in_bytes': 5642, 'id': 5, 'created_at': 1655707147.2081053, 'name': '1566389294_04414_pic', 'folder': '/home/amir/Desktop/Fruits', 'content': 'apple vase'}]
    #
    # cleaned = list(map(process_docs, docs, "db"))
    # print(cleaned)
    # uris = [('QmT5j2ezeyngwzkt3iGYHgBqcukzyF3S6XNTSrjbGTJ1Nq',)]
    # valid_uris = list(filter(lambda x: len(x[0]) == 46, uris))
    # print(valid_uris)
    from datetime import datetime

    created_time = "2022-08-18T06:36:23+00:00"
    # dated = datetime.fromisoformat(created_time)
    # print(dated)
    from dateutil.parser import parse
    print(datetime.now())
    get_date_obj = parse(created_time)
    # print(datetime.now()-get_date_obj)
    # print(get_date_obj)