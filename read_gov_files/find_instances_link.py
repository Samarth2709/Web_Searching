import pandas as pd
import os
import numpy as np
import math
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException



def read_df(filename, sheet_name = "Sheet1"):
    df = pd.read_excel(filename, sheet_name = sheet_name)
    return df


def get_col(df, col_name):
    return list(df[col_name])


def get_html_source_code(doc_url:str) -> str:
    url = doc_url
    # time.sleep(2)
    print(url)
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


def check_string_in_file(webpage_text:str, substring:str) -> int:
    if substring in webpage_text:
        return webpage_text.lower().count(substring.lower())
    else:
        return 0


def format_link(link):
    if "document" in link.lower() and 'htm' in link.lower():
        # https://sec.report/Document/0001213900-21-007575/ea134595-s1_aceglobal.htm
        return "only_doc" + link.replace('/', '&').replace('?', '!')[link.index('D'):-4] + ".txt"
    elif "document" in link.lower() and 'htm' not in link.lower():
        # https://sec.report/Document/0001193125-20-195583/
        return "no_htm" + link.replace('/', '&').replace('?', '!')[link.index('D'):] + ".txt"
    return "norm" + link.replace('/', '&').replace('?', '!')[20:-4] + ".txt"
    # original / are &
    # original ? are  !
    # norm means link is sec.gov and htm
    # no_htm means it is document with no htm
    # only_doc means it is only document type and has htm

def revert_format(link):
    if "only_doc" in link:
        return 'https://sec.report/' + link.replace('&', '/').replace('!', '?')[8:-4] + '.htm'
    elif "no_htm" in link:
        return 'https://sec.report/' + link.replace('&', '/').replace('!', '?')[6:-4]
    elif "norm" in link:
        return 'https://www.sec.gov/' + link.replace('&', '/').replace('!', '?')[4:-4] + '.htm'
    else:
        print(link, "is not a valid formated link")
        return

def get_words_after_instance(site_text, key_word):
    if key_word in site_text:
        key_word_index = site_text.index(key_word)
        paragraph_text = site_text[key_word_index:key_word_index+100]
        list_site_words = paragraph_text.split(' ')
        return ' '.join(list_site_words[:8])
    return None


start_time = time.time()

chrome_options = Options()
chrome_options.add_argument("--window-size=1024x768")
chrome_options.add_argument("--headless")
chrome_options.add_argument('disable-blink-features=AutomationControlled')
chrome_options.add_argument('user-agent=Type user agent here')
driver = webdriver.Chrome(options=chrome_options, executable_path='C:\Webdriver\chromedriver.exe')


filename = "SEC Filings Python Pull.xlsx"
df = read_df(filename, sheet_name="Sheet2")
url_col = np.array(get_col(df, "Sec Filings "))

count_col = []
# sponsor
sponsor_string_col = []
for i, link in enumerate(url_col):
    print(str(i+1) + "/" + str(len(list(url_col))))

    # Checks if cell in url_col is a link
    if "sec" not in str(link):
        count_col.append("Not Link")
        continue
    # *********

    # Checks if https in link if not adds it to link
    if "https" not in str(link):
        link = "https://www." + link
    # *******

    # Makes sure website_text is valid and has good data
    while True:
        website_text = get_html_source_code(link)
        if "Your Request Originates from an Undeclared Automated Tool" in website_text:
            print("Bad Request")
            continue
        else:
            break
    count_col.append(check_string_in_file(webpage_text=website_text, substring="indicated an interest"))
    # string_after_sponsor = get_words_after_instance(website_text, "sponsor")
    # sponsor_string_col.append(string_after_sponsor)
driver.close()

df["Count Indicated an Interest"] = pd.Series(np.array(count_col))
# df["String After Sponsor"] = pd.Series(np.array(sponsor_string_col))

df.to_excel(filename[:-5]+'(OUTPUT)Indicated.xlsx', index=False)
print("SAVED")

hr, minu, sec = format_time(time.time() - start_time)
print("Hours: " + str(hr) + "\nMinutes: " + str(minu) + "\nSeconds: " + str(sec))



