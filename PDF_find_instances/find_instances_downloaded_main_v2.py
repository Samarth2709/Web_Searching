import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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


def format_time(secs):
    second = round(secs)
    if secs > 60:
        minutes = round(second/60)
        second_left = second%60
        return minutes, second_left
    else:
        return 0, second


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


start_time = time.time()

chrome_options = Options()
chrome_options.add_argument("--window-size=1024x768")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options, executable_path='C:\Webdriver\chromedriver.exe')


filename = "Python Pull PDF.xlsx"
df = read_df(filename)
url_col = get_col(df, "SEC (Temp)")

output_numb_occurences = []
# Get numb instances of forward purchase in each link
for i, link in enumerate(url_col):
    print(str(i+1) + "/" + str(len(url_col)))
    sleep_time = 45

    # Checks if cell in url_col is a link
    if "https://" not in str(link):
        output_numb_occurences.append(0)
        continue

    # Makes sure website_text is valid
    while True:
        website_text = get_html_source_code(link)
        time.sleep(sleep_time)
        if "Your Request Originates from an Undeclared Automated Tool" in website_text:
            print("Bad Request")
            sleep_time = sleep_time+30
            print(sleep_time)
            continue
        else:
            break

    numb_instance = check_string_in_file(webpage_text=website_text, substring="forward purchase")
    output_numb_occurences.append(numb_instance)
    print("Number Instances: " + str(numb_instance))
    time.sleep(5)

driver.close()

df["Number instance"] = pd.Series(np.array(output_numb_occurences))

df.to_excel(filename[:-5]+'(OUTPUT).xlsx', index=False)
print("SAVED")

minu, sec = format_time(time.time() - start_time)
print("Minutes: " + str(minu) + "\nSeconds: " + str(sec))



