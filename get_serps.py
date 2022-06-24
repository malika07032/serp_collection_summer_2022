import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from time import sleep
import time, os
from datetime import datetime
import csv
import sys

# Set the driver path
driverpath ='driver/chromedriver'
chrome_options = webdriver.ChromeOptions()

### from youtube2 code (Ropah)
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
desired_cap = chrome_options.to_capabilities()

def get_serp_by_query(query, serp_folder_path):
    """
    This function can search Google for query.
    Parameters:
    query - a string that contains the phrase that will be searched
    serp_folder_path - a path to folder where resulting serps are saved
    """
    # Create a new instance of the driver for every search
    driver = webdriver.Chrome(executable_path=driverpath, 
                              options=chrome_options)
    
    # perform the search, because we need the location link to show
    url = f"https://google.com/search?q={query}"
    driver.get(url)
    sleep(2)
    # Access the content of the page
    htmlPage = driver.page_source
    filename = query.replace('/','')
    with open(f"{serp_folder_path}/{filename}.html", 'w', encoding='utf-8') as output:
        output.write(htmlPage)
    driver.close()

def search_all_queries(queries_file_csv):
    serp_folder_path = 'SERP_{}'.format(datetime.now())
    #if not os.path.isdir(serp_folder_path):
    os.mkdir(serp_folder_path)

    with open(queries_file_csv, 'r') as inputF:
        queries = []
        reader = csv.reader(inputF)
        for row in reader:
            queries.append(row[0])

    for query in queries:
        get_serp_by_query(query, serp_folder_path)

if __name__ == "__main__":
    search_all_queries(sys.argv[1])