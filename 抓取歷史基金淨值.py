from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import csv
import re

input_begin_date='2000/01/01'
input_end_date='2023/02/23'

Fund_codes=pd.read_excel('Fund Code.xlsx')
Fund_codes['Fund Ref'].fillna("NA", inplace=True)

#在背景抓取
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

for Fund, Fund_ref in zip(Fund_codes['Fund Code'],Fund_codes['Fund Ref']):

    #抓基金代號
    if Fund_ref == "NA":

        url="https://tw.stock.yahoo.com/fund/search?onshore=2&sortBy=return3M&q="+ Fund +"&morningStarRanking=0&currencyId=CU%24%24%24%24%24USD&return3M=0"
        chrome = webdriver.Chrome(options=options)
        chrome.get(url)
        soup = BeautifulSoup(chrome.page_source, "lxml")

        pattern = re.compile('.*{}.*'.format(Fund[:6]))
        # 找出所有title包含目標文字的連結
        soup_links = soup.find_all("a", {"title": pattern})
        # 取出第一個符合條件的連結
        soup_fund = soup_links[0] if soup_links else None

        if soup_fund is None:
            no=int(len(Fund) * 0.4)
            url = "https://tw.stock.yahoo.com/fund/search?onshore=2&sortBy=return3M&q=" + Fund[:no] + "&morningStarRanking=0&currencyId=CU%24%24%24%24%24USD&return3M=0"
            chrome = webdriver.Chrome(options=options)
            chrome.get(url)
            soup = BeautifulSoup(chrome.page_source, "lxml")

            pattern = re.compile('.*{}.*'.format(Fund[:6]))
            # 找出所有title包含目標文字的連結
            soup_links = soup.find_all("a", {"title": pattern})
            # 取出第一個符合條件的連結
            soup_fund = soup_links[0] if soup_links else None

            if soup_fund is None:
                print(Fund,url)
                continue
        else:
            fund_ref = soup_fund['href']
            fund_code = fund_ref.split('/')[-1]
            Fund_ref=fund_code
            Fund_codes.loc[Fund_codes['Fund Code'] == Fund, 'Fund Ref'] = fund_code
            Fund_codes.to_excel('Fund Code.xlsx', index=False)

    #抓取歷史淨值
    print(Fund,str(Fund_ref))
    url = 'https://tw.stock.yahoo.com/fund/history/' + Fund_ref
    chrome = webdriver.Chrome()#"./goolemapSpider/chromedriver.exe",
    chrome.get(url)
    time.sleep(0.5)

    begin_date = chrome.find_element(By.CSS_SELECTOR, 'input[placeholder="開始年月"]')
    end_date = chrome.find_element(By.CSS_SELECTOR, 'input[placeholder="結束年月"]')
    begin_date.send_keys(Keys.CONTROL + "a")
    begin_date.send_keys(Keys.DELETE)
    end_date.send_keys(Keys.CONTROL + "a")
    end_date.send_keys(Keys.DELETE)
    time.sleep(0.5)
    begin_date.send_keys(input_begin_date)
    time.sleep(0.5)
    end_date.send_keys(input_end_date)
    time.sleep(0.5)
    download_button = chrome.find_element(By.XPATH, "//button[text()='下載']")
    download_button.click()

    time.sleep(3)

    # 下載檔案
    old_file_path = 'C:\\Users\Arlen\Downloads'
    new_file_path = 'C:\\Users\Arlen\Desktop\GitHub\Value Investing by Python\History Data'
    old_file_name = (Fund_ref).replace(':', "_")
    new_file_name = (Fund + '.csv')

    #判斷檔案是否下載完成，並更名存檔
    check = 0
    while check == 0:
        if os.path.exists(os.path.join(old_file_path, old_file_name)):
            with open(os.path.join(old_file_path, old_file_name), 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                rows = []
                for row in reader:
                    rows.append(row)

            header[0] = 'Date'
            header[1] = 'Close'
            header[2] = 'Diff'
            header[3] = 'Persent'

            with open(os.path.join(new_file_path, new_file_name), 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(rows)

            os.remove(os.path.join(old_file_path, old_file_name))
            break
        else:
            time.sleep(3)
