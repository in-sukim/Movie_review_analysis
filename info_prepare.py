import re 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import warnings
warnings.filterwarnings('ignore')

from selenium.webdriver.common.keys import Keys
import time
def get_movie_info(keyword):
    url = 'https://movie.daum.net/main'
    driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(2)

    driver.find_element(By.XPATH , '//*[@id="mainContent"]/div/div[1]/form/fieldset/div/input').send_keys(keyword)
    driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[1]/form/fieldset/div/button').click()
    time.sleep(2)


    driver.find_element(By.CLASS_NAME, 'thumb_img').click()
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'txt_tabmenu').click()

    total_info = driver.find_element(By.CLASS_NAME, 'detail_cont').text.split('\n')[:-1]
    type_list = []
    info_list = []
    for i in range(len(total_info)):
        info_list.append(': '.join(total_info[i].split()))

    breif_story = driver.find_element(By.CLASS_NAME,'desc_cont').text
    actors_list = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[2]/div[2]/div[2]/ul')
    actors = actors_list.find_elements(By.TAG_NAME,'li')


    crew_name = []
    crew_position = []
    for i in actors:
        crew_name.append(i.text.split('\n')[0])
        crew_position.append(i.text.split('\n')[1])

    return info_list, breif_story, crew_name, crew_position

# type_list, info_list,breif_story, crew_name, crew_position = get_movie_info('존윅4')
