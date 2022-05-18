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
import os
import re
from pathlib import Path

parent_path = 'enwiki-20220301-pages-meta-history13_html'
filenames = next(
    os.walk(os.path.join(parent_path)), (None, None, []))[2]
count = 1
i = 1
for file in (filenames):
    with open(parent_path + "/" + file, "r+") as f:
        text = f.read()
        if "image_link" in text:
            print(i, "'"+file+"',")
            i += 1

# import re
#
# string = '<img src=https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5t_JKlO_W8VjkAvmJOvTUDfZwwAJ9Ry9QmSG8OJXZpB098JD1-CGcFryWq2A&s alt="Thumbnail" style="height: 300px; width: 300px; object-fit: contain;"/>'
# ip_regex = re.search(r"(?<=src=)(.*)(?= alt=)", string).group(1)
# print(ip_regex)

