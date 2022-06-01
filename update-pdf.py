import os
import re

import pdfkit

data_folder = '/home/amir/Desktop/Unused Data/enwiki-20220301-pages-articles-multistream1_html'
target_folder = '/home/amir/Desktop/Requests-Images/enwiki-20220301-pages-articles-multistream1_html/enwiki-20220301-pages-articles-multistream1_html'
filenames = next(os.walk(target_folder), (None, None, []))[2]
# filenames = filenames[:1000]
for index, file in enumerate(filenames):
    options = {
        "page-size": "Letter",
        "margin-top": "0.0in",
        "margin-right": "0.0in",
        "margin-bottom": "0.0in",
        "margin-left": "0.0in",
    }
    if ".pdf" in file:
        print(index, file)
        target_folder_html_path = f"{target_folder}/{file.replace('.pdf', '.html')}"
        target_folder_pdf_path = f"{target_folder}/{file}"
        with open(data_folder + "/" + file.replace(".pdf", '.html'), "r+") as f:
            text = f.read()
            regex = r"(?<=<div class=\"right-element\")((.|\n)*)(?=</div>)"
            subst = ""
            result = re.sub(regex, subst, text, 1)
            text = result.replace('<div class="right-element"', '')
            with open(target_folder_html_path, 'w+') as html_file:
                html_file.write(text)
                html_file.close()

            os.remove(target_folder_pdf_path)
            pdfkit.from_file(
                f"{target_folder_html_path}",
                f"{target_folder_pdf_path}",
                options=options,
            )
            os.remove(target_folder_html_path)