import codecs
import datetime
import os
import subprocess
import traceback
import xml.sax
from multiprocessing.pool import ThreadPool

from tinydb import TinyDB
import mwparserfromhell
import re
from dotenv import load_dotenv

load_dotenv()

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6})|[style|class|align]+=.*')

html_template = """<!DOCTYPE html>
<html>
<body>
<style>
.container {
    width:800px;
    position: absolute;
}

.left-element {
    display: inline-block;
    position: absolute;
    left: 0;
    margin-right:50px;
    padding:5px;

}
</style>

<div class="container">
    <div class="left-element">
        <h1>%s</h1>
        <p>%s</p>
        <h3> Properties </h3>
        <p> %s</p>
        <h3> Wikilinks </h3>
        <p> %s</p>
        <h3> External Links </h3>
        <p>%s</p>
    </div>
</div>

</body>
</html>"""


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def clean_text(text):
    clean_text = text.replace("{{", " ").replace("}}", " ").replace("|", "").replace("''", "").replace("[[",
                                                                                                       " ").replace("*",
                                                                                                                    "") \
        .replace("*", "").replace("]]", " ").replace("==", " ").replace("!", "") \
        .replace("{", "").replace("}", "").replace(";", "").replace("-", " ").replace("short description", "")
    return clean_text


class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Content handler for Wiki XML data using SAX"""

    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []
        self._article_count = 0
        self._books = []
        self.CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    def cleanhtml(self, raw_html):
        cleantext = re.sub(self.CLEANR, '', raw_html)
        return cleantext

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            # cleantext = BeautifulSoup(content, "html.parser").text
            cleantext = self.cleanhtml(content)
            self._buffer.append(cleantext)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text'):
            self._current_tag = name
            self._buffer = []

    def process_article(self, title, text, template='all'):
        """Process a wikipedia article looking for template"""

        # Create a parsing object
        wikicode = mwparserfromhell.parse(text)

        # Search through templates for the template
        matches = wikicode.filter_templates()

        if len(matches) >= 1:
            # Extract information from infobox
            properties = {param.name.strip_code().strip(): param.value.strip_code().strip()
                          for param in matches[0].params
                          if param.value.strip_code().strip()}

            # Extract internal wikilinks
            wikilinks = [x.title.strip_code().strip() for x in wikicode.filter_wikilinks()]
            # Extract external links
            exlinks = [x.url.strip_code().strip() for x in wikicode.filter_external_links()]
            return title, text, properties, wikilinks, exlinks

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)
        if name == 'page':
            self._article_count += 1
            # Send the page to the process article function
            title = self._values.get("title", None)
            text = self._values.get("text", None)

            book = self.process_article(title=title, text=text,
                                        template='all')
            # If article is a book append to the list of books
            if book:
                self._books.append(book)


def pool_code(func, sub_link, pool_number):
    chunks_list = []
    for i in range(0, len(sub_link), 20):
        chunk = sub_link[i: i + 20]
        chunks_list.append(chunk)
    pool_size = pool_number
    pool = ThreadPool(pool_size)
    pool.map(func, chunks_list)
    pool.close()
    pool.join()
    print("done pooling")


def pool_func(books):
    db = TinyDB(f"db/{output_file_name}.json")
    for article in books:
        try:
            title = article[0]
            raw_text = article[1].replace("===", "")
            clean_text_html = cleanhtml(raw_text)
            if "/" in title:
                title = title.replace("/", " ")
            f = codecs.open(text_file_path + "/" + str(title) + ".html", "w+", "utf-8")
            text = clean_text(clean_text_html)
            br_text = text.replace("\n", "<br>")
            properties = article[2] if article[2] else ""
            wikilinks = article[3]
            exlinks = article[4]
            if wikilinks:
                wikilinks = "<br>".join(wikilinks)
            else:
                wikilinks = ""
            if exlinks:
                exlinks = "<br>".join(exlinks)
            else:
                exlinks = ""
            db.insert({"title": title, "content": str(text)})
            image_link = 'image_link alt="Thumbnail" style="height: 300px; width: 300px; object-fit: contain;"'
            output_text = html_template % (title, br_text,
                                           properties, wikilinks,
                                           exlinks, image_link)
            f.write(str(output_text))
            f.close()
        except:
            traceback.print_exc()
            continue
    print("done")


if __name__ == '__main__':
    print(datetime.datetime.utcnow())
    ZIP_FILE_PATH = os.getenv('ZIP_FILE_PATH')
    if ZIP_FILE_PATH:
        filename = ZIP_FILE_PATH
    else:
        filename = 'enwiki-20220601-pages-articles-multistream15.xml-p17324603p17460152.bz2'
    output_file_name = "-".join(filename.split("-")).split(".")[0].split("/")[-1]
    text_file_path = f"/home/umair/FinDe/Script_Data/{output_file_name}_html"

    if not os.path.isdir(text_file_path):
        os.mkdir(text_file_path)

    if not os.path.isdir("db"):
        os.mkdir("db")
    # db = TinyDB(f"db/{output_file_name}.json")

    # Object for handling xml
    handler = WikiXmlHandler()
    # Parsing object
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    # Iteratively process file
    print(filename)
    for line in subprocess.Popen(['bzcat'],
                                 stdin=open(filename),
                                 stdout=subprocess.PIPE).stdout:
        parser.feed(line)

        # Stop when 3 articles have been found
        # if len(handler._pages) > 5:
        #     break

    books = handler._books

    print(f'\nSearched through {handler._article_count} articles.')
    db_list = []
    for article in books:
        title = article[0]
        raw_text = article[1].replace("===", "")
        clean_text_html = cleanhtml(raw_text)
        if "/" in title:
            title = title.replace("/", " ")
        if len(title) > 100:
            title = title.split(" ")[:5]
            file_name = " ".join(title)
        else:
            file_name = title
        f = codecs.open(text_file_path + "/" + str(file_name) + ".html", "w+", "utf-8")
        text = clean_text(clean_text_html)
        br_text = text.replace("\n", "<br>")
        properties = article[2] if article[2] else ""
        wikilinks = article[3]
        exlinks = article[4]
        if wikilinks:
            wikilinks = "<br>".join(wikilinks)
        else:
            wikilinks = ""
        if exlinks:
            exlinks = "<br>".join(exlinks)
        else:
            exlinks = ""
        db_list.append({"title": title, "content": text})
        # db.insert({"title": title, "content": text})
        # image_link = 'image_link alt="Thumbnail" style="height: 300px; width: 300px; object-fit: contain;"'
        output_text = html_template % (title, br_text,
                                       properties, wikilinks,
                                       exlinks)
        f.write(str(output_text))
        f.close()
    # db.insert_multiple(db_list)
    print(datetime.datetime.utcnow())
    # pool_code(pool_func, books, 10)
