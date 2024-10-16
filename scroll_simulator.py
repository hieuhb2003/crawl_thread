import time
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import randint
THREAD_URL = 'https://www.threads.net/'
WAIT_TIMEOUT = 5  
chrome_options = Options()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

driver.get(THREAD_URL)

# Tải cookie từ file
cookies = pickle.load(open("my_cookie.pkl", "rb"))

# Thêm cookie vào phiên làm việc của Selenium
for cookie in cookies:
    driver.add_cookie(cookie)
driver.refresh()
# driver = webdriver.Chrome()
# driver.get(THREAD_URL)
time.sleep(WAIT_TIMEOUT)

def scoll_and_get_list(num):
    page = BeautifulSoup(driver.page_source, features="html.parser")
    count = 0
    href_list = []
    while(count < num):
        divs_with_href = page.find_all("a", {"href": lambda href: href and href.startswith("/@") and "/post/" in href})
        for div in divs_with_href:
            href_list.append(THREAD_URL + div['href'])
        # driver.execute_script(f"window.scrollBy(0, {half_scroll_distance});") 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(15)
        
        # time.sleep(randint(3, 5))
        count += 1
    driver.close()
    return list(set(href_list))

# hef_list = scoll_and_get_list()
# for href in hef_list:  
#     print(href)
# print(len(hef_list))
# num = 2
# print(scoll_and_get_list(num))