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
chrome_options.add_experimental_option("prefs", { "profile.default_content_settings.geolocation": 1})
desired_cap = chrome_options.to_capabilities()

def get_serp_by_query(query, coordinatesDict, locationName):
    """
    This function can search Google for query.
    Parameters:
    query - a string that contains the phrase that will be searched
    serp_folder_path - a path to folder where resulting serps are saved
    """
    # Create a new instance of the driver for every search
    driver = webdriver.Chrome(executable_path=driverpath, 
                              options=chrome_options)

     # setup the new coordinates
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", 
                           coordinatesDict)
    
    # perform the search, because we need the location link to show
    url = f"https://google.com/search?q={query}"
    driver.get(url)

    # find the link that will help update the location
    try:
        driver.find_element_by_css_selector("update-location").click()
    except:
        # sometimes, the page is not loaded, so we'll wait and try again
        sleep(2)
        driver.find_element_by_css_selector("update-location").click()

    sleep(3)
    # Access the content of the page
    htmlPage = driver.page_source
    #filename = f"{query.replace('/','')}_{locationName}"
    with open(f"pizza_results/{locationName}.html", 'w', encoding='utf-8') as output:
        output.write(htmlPage)
    driver.close()

def search_all_queries(queries_file_csv):
    #serp_folder_path = 'SERP_{}'.format(datetime.now())
    #os.mkdir(serp_folder_path)
    os.mkdir('pizza_results')
    locations = {'CA-Alameda': {'latitude': 37.765205, 'longitude': -122.241638, 'accuracy': 100},
    'OH-Youngstown': {'latitude': 41.10297, 'longitude': -80.647247, 'accuracy': 100},
    'VA-Hampton': {'latitude': 37.034946, 'longitude': -76.360123, 'accuracy': 100},
    'NJ-Union': {'latitude': 40.702503, 'longitude': -74.261398, 'accuracy': 100},
    'NY-Auburn': {'latitude': 42.933334, 'longitude': -76.566666, 'accuracy': 100}}

    query = 'pizza'
    for location in locations:
        get_serp_by_query(query, location, 'CA-Alameda')
    #with open(queries_file_csv, 'r') as inputF:
        
        #queries = []
        #reader = csv.reader(inputF)
        #for row in reader:
            #queries.append(row[0])

    #for query in queries:
        #get_serp_by_query(query, location, 'CA-Alameda')

if __name__ == "__main__":
    search_all_queries(sys.argv[1])