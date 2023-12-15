import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# import selenium
import time
import re
import pandas as pd



driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
job_dict = {}

for page_no in range(1, 26):
    print('scraping page: ', page_no)
    url = f'https://www.seek.com.au/data-jobs?page={page_no}'
    print(url)
    driver.get(url)
    job_cards = driver.find_elements(By.XPATH, '//a[@data-automation="jobTitle"]')
    job_links = [card.get_attribute('href') for card in job_cards]

    for link in job_links:

        # link = card.get_attribute('href')
        print(link)
        job_id = re.search(r"job/(\d+)", link).group(1)
        # print(job_id)
        # card.click()
        driver.get(link)
        # time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_detail = soup.find('div', {'data-automation': 'jobAdDetails'}).get_text()
        job_dict[job_id] = {'job_detail': job_detail}
        # print(job_id)
        # print(card.text)
        # print('@'*50)


driver.close()
# print(job_dict)

df = pd.DataFrame.from_dict(job_dict, orient='index', columns=['job_detail'])
df = df.reset_index().rename(columns={'index': 'job_id'})
df.to_csv('job_detail.csv', index=False)