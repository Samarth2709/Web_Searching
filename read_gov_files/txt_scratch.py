import pandas as pd
import os
import numpy as np
import math
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def read_df(filename, sheet_name = "Sheet1"):
    df = pd.read_excel(filename, sheet_name = sheet_name)
    return df


def get_col(df, col_name):
    return list(df[col_name])


def get_html_source_code(doc_url:str) -> str:
    url = doc_url
    time.sleep(2)
    driver.get(url)
    text_stuff = str(driver.find_element_by_xpath("/html/body").text)
    return text_stuff


def format_time(secs):
    second = round(secs)
    if secs > 3600:
        hours = math.floor(secs / 3600)
        minutes = math.floor((secs % 3600)/60)
        second_left = second % 60
        return hours, minutes, second_left
    elif secs > 60:
        minutes = round(second/60)
        second_left = second%60
        return 0, minutes, second_left
    else:
        return 0, 0, second


def convert_to_txt(save_as_file:str, document_string:str, dir = r"C:\Users\samar\Desktop\Web_Searching\read_gov_files\txt_files_of_gov"):
    path = os.path.join(dir, save_as_file)
    txt_file = open(path, "w+", encoding='utf-8')
    txt_file.truncate(0)
    txt_file.write(document_string)
    txt_file.close()


def format_link(link):
    return link.replace('/', '-')[20:-4] + ".txt"
    # take out


def get_link_dir(dir):
    pass


def is_element_appeared(element_Xpath, timeout = 30):
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, element_Xpath)))
        return True
    except TimeoutException:
        raise RuntimeError("Something went wrong!!")
        return False


start_time = time.time()

chrome_options = Options()
chrome_options.add_argument("--window-size=1024x768")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options, executable_path='C:\Webdriver\chromedriver.exe')



filename = "Python Pull PDF.xlsx"
df = read_df(filename)
url_col = get_col(df, "SEC (Temp)")

for i, link in enumerate(url_col):
    print(str(i+1) + "/" + str(len(url_col)))
    sleep_time = 45

    # Checks if cell in url_col is a link
    if "https://" not in str(link):
        continue

    # Makes sure website_text is valid
    while True:
        website_text = get_html_source_code(link)
        time.sleep(sleep_time)
        if "Your Request Originates from an Undeclared Automated Tool" in website_text:
            print("Bad Request")
            sleep_time += 30
            print(sleep_time)
            continue
        else:
            break
    save_link = format_link(link)
    convert_to_txt(save_link, website_text)

    time.sleep(5)

driver.close()



hr, minu, sec = format_time(time.time() - start_time)
print("Hours: " + str(hr) + "\nMinutes: " + str(minu) + "\nSeconds: " + str(sec))



