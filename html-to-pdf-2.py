import datetime
import os
import re
import traceback
from multiprocessing.pool import ThreadPool
import pdfkit as pdfkit


def html_to_pdf(files):
    options = {
        "page-size": "Letter",
        "margin-top": "0.0in",
        "margin-right": "0.0in",
        "margin-bottom": "0.0in",
        "margin-left": "0.0in",
    }
    for html_file in files:
        global count
        count += 1
        print(count, html_file)
        target_folder_html_path = f"{destination_folder}/{html_file}"
        target_folder_pdf_path = f"{destination_folder}/{html_file.replace('.html', '.pdf')}"
        if ".pdf" in html_file:
            continue
        try:
            with open(f"{parent_path}/{html_file}", "r+") as f:
                text = f.read()
                regex = r"(?<=<div class=\"right-element\")((.|\n)*)(?=</div>)"
                subst = ""
                result = re.sub(regex, subst, text, 1)
                text = result.replace('<div class="right-element"', '')
            with open(f"{target_folder_html_path}", 'w+') as html_file:
                html_file.write(text)
                html_file.close()

            pdfkit.from_file(
                f"{target_folder_html_path}",
                f"{target_folder_pdf_path}",
                options=options,
            )
            os.remove(target_folder_html_path)
        except:
            print(html_file)
            traceback.print_exc()


def remove_files(files):
    for html_file in files:
        global count
        print(count, html_file)
        count += 1
        if ".pdf" in html_file:
            continue
        try:
            updated_file = html_file.replace(".html", "")
            # print(f"{destination_folder}/{updated_file}.pdf")
            os.remove(f"{destination_folder}/{updated_file}.pdf")
        except:
            traceback.print_exc()


def pool_code(func, sub_link, pool_number):
    chunks_list = []
    for i in range(0, len(sub_link), 5):
        chunk = sub_link[i: i + 5]
        chunks_list.append(chunk)
    pool_size = pool_number
    pool = ThreadPool(pool_size)
    pool.map(func, chunks_list)
    pool.close()
    pool.join()
    print("done pooling")


def remove_image_tag_html(files):
    for file in files:
        with open(parent_path + "/" + file, "r+") as f:
            text = f.read()
            regex = r"(?<=<div class=\"right-element\")((.|\n)*)(?=</div>)"
            subst = ""
            result = re.sub(regex, subst, text, 1)
            text = result.replace('<div class="right-element"', '')
            f = open(f"{destination_folder}/{file}", "w")
            f.write(text)
            f.close()


if __name__ == '__main__':
    # Run this once current script finishes
    folders_list = [
        ("/home/amir/Desktop/Complete Scraped Data 18-05-2022/enwiki-20220301-pages-meta-current2-pdf",
         "/home/amir/Desktop/Complete Scraped Data 18-05-2022/enwiki-20220301-pages-meta-current2_html"),

    ]
    for folder in folders_list:
        # destination_folder = "/home/amir/Desktop/Only PDFs/enwiki-20220301-pages-articles-multistream14_html"/home/amir/Desktop/Unused Data/enwiki-20220301-pages-articles-multistream21_html
        # parent_path = '/home/amir/Desktop/Unused Data/enwiki-20220301-pages-articles-multistream14_html'
        destination_folder = folder[0]
        parent_path = folder[1]
        print(datetime.datetime.utcnow())
        count = 1
        filenames = next(
            os.walk(parent_path), (None, None, [])
        )[2]
        # filenames = filenames[226861:]
        pool_code(html_to_pdf, filenames, 25)
        # remove_files(filenames)
        # html_to_pdf(["MDI.html"])
        print(datetime.datetime.utcnow())
