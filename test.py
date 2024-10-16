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

# # Tải cookie từ file
# cookies = pickle.load(open("my_cookie.pkl", "rb"))

# # Thêm cookie vào phiên làm việc của Selenium
# for cookie in cookies:
#     driver.add_cookie(cookie)
# driver.refresh()
# driver = webdriver.Chrome()
# driver.get(THREAD_URL)
time.sleep(WAIT_TIMEOUT)

# Scroll to the end of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Optionally wait for the page to load more content (if using infinite scroll)
time.sleep(2)

# Close the driver
driver.quit()