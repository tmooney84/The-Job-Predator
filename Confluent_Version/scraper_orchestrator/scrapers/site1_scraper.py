from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape():
    options = webdriver.ChromeOptions()
    # Comment out headless for testing:
    # options.add_argument('--headless')

    service = Service()  # assumes chromedriver is in PATH
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome()


    url = "http://quotes.toscrape.com"
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "quote"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    quote_blocks = soup.find_all('div', class_='quote')
    results = []

    for quote_block in quote_blocks:
        text = quote_block.find('span', class_='text').get_text(strip=True)
        author = quote_block.find('small', class_='author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote_block.find_all('a', class_='tag')]

        results.append({
            "text": text,
            "author": author,
            "tags": tags
        })

    return results

if __name__ == "__main__":
    for quote in scrape():
        print(quote)
