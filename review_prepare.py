#!/usr/bin/env python
# coding: utf-8

# In[2]:

import re 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import pandas as pd
import numpy as np
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

from selenium.webdriver.common.keys import Keys

#
# In[1]:

def preprocess(df):
    texts = []
    for i in tqdm(df['text']):
        text = re.sub('[^0-9a-zA-Z가-힣\s]', ' ', i)
        texts.append(str(text))
    
    df['text'] = texts
    return df
# webdriver.ChromeOptions() headless 옵션 추가 시 element not found error 발생(수정 필요)
def daum(keyword, num: int):
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')

    url = 'https://movie.daum.net/main'
    driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
#     driver.implicitly_wait(10)
    driver.get(url)
    time.sleep(2)

    # 검색어 입력
    
    driver.find_element(By.XPATH , '//*[@id="mainContent"]/div/div[1]/form/fieldset/div/input').send_keys(keyword)
    driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[1]/form/fieldset/div/button').click()
    time.sleep(2)

    # 검색 리스트 중 가장 위의 영화(검색 영화) 선택
    driver.find_element(By.CLASS_NAME, 'thumb_img').click()
    time.sleep(5)
    # time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a').click()
    time.sleep(5)
    # time.sleep(3)

    for i in range(num):
        driver.find_element(By.XPATH, '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button').click()
        time.sleep(3)

    items = driver.find_element(By.XPATH,'//*[@id="alex-area"]/div/div/div/div[3]/ul[2]')
    li = items.find_elements(By.TAG_NAME, 'li')

    li_list = []
    for i in li:
        li_list.append(i.text)

    idx = [2, 3]
    reviews = []
    for i in tqdm(li_list, desc = '리뷰 전처리 중'):
        step1 = i.split('\n')
        step2 = np.array(step1)[idx].tolist()
        reviews.append(step2)
    
    df = pd.DataFrame(reviews).rename(columns = {0:'rating',1:'text'})
    df = df.loc[df['text'].str.len() > 7]
    
    
    
    return preprocess(df)