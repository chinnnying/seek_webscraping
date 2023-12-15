import requests
from bs4 import BeautifulSoup
import re


def scrape(pg):
    url = 'https://www.seek.com.au/data-jobs'
    # , 'https://www.seek.com.au/data-jobs?page={pg}']

    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers)
    

    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('article', {'data-card-type': 'JobCard'})

        return articles


    else:
        print('Failed to retrieve the webpage')



def extract_attr(article, data_automation_attributes):
    tag = article.find(lambda tag: tag.get('data-automation') == data_automation_attributes)
    return tag.get_text().strip() if tag else None



data_automation_attributes = ['jobTitle',
                                'jobCompany',
                                'jobLocation',
                                'jobSalary',
                                'shortDescription',
                                'jobClassification',
                                'jobSubClassification']


articles = scrape()

jobs_data = {
    
    article.get('data-job-id', None):
    {
        'job_title': extract_attr(article, 'jobTitle'),
        'company': extract_attr(article, 'jobCompany'),
        'location': extract_attr(article, 'jobLocation'),
        'salary': extract_attr(article, 'jobSalary'),
        'job_type': article.find('p', string=re.compile(r'\bjob\b', re.I)).get_text().strip(),
        'short_description': extract_attr(article, 'jobShortDescription'),
        'classification': extract_attr(article, 'jobClassification'),
        'sub_classification': extract_attr(article, 'jobSubClassification')
    }
    for article in articles
}

print(jobs_data)

