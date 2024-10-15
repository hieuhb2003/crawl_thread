from selenium import webdriver
import pickle
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import argparse

def login_and_save_cookies(username, password):
    browser = webdriver.Chrome()
    try:
        browser.get("https://www.threads.net/login")
        sleep(3)
        input_user = browser.find_element(By.XPATH, "//input[@placeholder='Username, phone or email']")
        input_user.send_keys(username)
        sleep(3)
        input_pass = browser.find_element(By.XPATH, "//input[@placeholder='Password']")
        input_pass.send_keys(password)
        sleep(1)
        input_pass.send_keys(Keys.ENTER)
        sleep(10)

        pickle.dump(browser.get_cookies(), open("my_cookie.pkl", "wb"))
        print("Cookies đã được lưu thành công.")

    finally:
        browser.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Đăng nhập vào Threads và lưu cookies.')
    parser.add_argument('-u', '--username', required=True, help='Username để đăng nhập')
    parser.add_argument('-p', '--password', required=True, help='Password để đăng nhập')

    args = parser.parse_args()

    login_and_save_cookies(args.username, args.password)

# script :
# python login.py -u "your_username" -p "your_password"