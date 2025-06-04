from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchAttributeException
import json
import re
import random

driver = webdriver.Chrome()
driver.get("https://www.ibm.com/careers/search?field_keyword_08%5B0%5D=Consulting&field_keyword_08%5B1%5D=Enterprise%20Operations&field_keyword_08%5B2%5D=Infrastructure%20%26%20Technology&field_keyword_08%5B3%5D=Software%20Engineering&field_keyword_05%5B0%5D=United%20States")

wait = WebDriverWait(driver, 20)

page_source = []

# Wait for first page to load
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bx--card__wrapper")))

while True:
    page_source.append(driver.page_source)

    try:
        # Wait for "Next" button to be clickable
        next_button = wait.until(EC.element_to_be_clickable(
            (By.ID, "IBMAccessibleItemComponents-next")
        ))

        # Click using JS to avoid interception issues
        driver.execute_script("arguments[0].click();", next_button)

        # Wait for new content to load
        time.sleep(random.randint(1,5))

        # Optional: Wait for job cards again (if needed)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bx--card__wrapper")))

    except:
        print("No more pages.")
        break

driver.quit()

page_source = ''.join(page_source)
soup = BeautifulSoup(page_source, 'html.parser')

job_cards = soup.find_all('div', class_="bx--card-group__cards__col")

import re

jobs = {
    'company': 'IBM',
    'title': [],
    'location': [],
    'category': [],
    'experience_level': [],
    'link' : []
}

pattern = r"^(Entry Level|Professional)"

for card in job_cards:
    raw_location = card.div.div.div.find('div', class_="ibm--card__copy__inner").text.strip()

    # Match experience level safely
    match = re.match(pattern, raw_location, flags=re.IGNORECASE)
    if match:
        experience_level = match.group(1)
        location = raw_location.replace(experience_level, '').strip()
    else:
        experience_level = "Unknown"
        location = raw_location  # leave full string as location
    jobs['link'].append(card.a['href'])
    jobs['title'].append(card['aria-label'])
    jobs['category'].append(card.div.div.div.div.text.strip())
    jobs['location'].append(location)
    jobs['experience_level'].append(experience_level)

#######!!! print worked once an has had trouble since
print(json.dumps(jobs, indent=2))