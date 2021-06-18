from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def get_part_of_long_ans(ans:str, is_date:bool, month_bool:bool, numb_bool:bool):
    if len(ans) > 25 and is_date == True:
        select_words = ans.split(" ")
        if month_bool == True:
            for month in months:
                if month in select_words:
                    where_month = select_words.index(month)
                    break
            if where_month<=7:
                return " ".join(select_words[:where_month+5])
            elif where_month>7 and len(select_words) - where_month >7:
                return " ".join(select_words[where_month-5:where_month+6])
            elif where_month>7 and len(select_words) - where_month <= 7:
                return " ".join(select_words[where_month - 5:])
            else:
                return " ".join(select_words)
# enter your code
chrome_options = Options()
chrome_options.add_argument("--window-size=1024x768")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options, executable_path='C:\Webdriver\chromedriver.exe')
months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def ask_google(query):
    is_date = False
    month_bool = False
    numb_bool = False

    # Search for query
    if len(query) < 3:
        return None

    query = query.replace(' ', '+')

    driver.get('http://www.google.com/search?q=' + query)

    # Get text from Google answer box

    answer = driver.execute_script("return document.elementFromPoint(arguments[0], arguments[1]);", 350, 230).text

    if "did not match any documents" in answer.lower() or len(answer) > 100:
        is_date = False

    for month in months:
        if month in answer.lower():
            is_date = True
            month_bool = True
            break

    # numidx = next((i for i, s in enumerate("dwojdwaf") if s.isdigit()), None)

    if is_date == False:
        for i, char in enumerate(answer):
            if char.isdigit():
                if answer[i:i+2].isdigit():
                    is_date = True
                    numb_bool = True
                    break

    if "Our systems have detected unusual traffic from your computer network".lower() in answer.lower():
        print("Our systems have detected unusual traffic from your computer network")
        time.sleep(30)

    # select area of answer if long



    if is_date:
        return answer
    else:
        return None

print(len("1990, New York, NY"))


