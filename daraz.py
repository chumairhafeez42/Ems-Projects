import traceback

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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
            traceback.print_exc()


if __name__ == '__main__':
    driver = run_chrome_over_server()
    driver.maximize_window()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/86.0.4240.75 Safari/537.36'}

    # r = requests.get('https://www.daraz.pk/#hp-just-for-you', headers=headers)
    driver.get('https://www.daraz.pk/#hp-just-for-you')

    # soup = BeautifulSoup(r.text, 'html.parser')
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    divs = soup.find_all('div', {"class":"card-jfy-item-wrapper hp-mod-card-hover J_Items inline"})
    for div in divs:
        title = div.find("div", {"class":"card-jfy-title"}).text.strip()
        price = soup.find("div", {"class":"hp-mod-price"}).div.text.strip()
        print(title, price)

