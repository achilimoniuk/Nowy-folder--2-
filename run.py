# Import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
import json
# Load .env file
import os
from dotenv import load_dotenv
load_dotenv()

# Defining class 
class QuoteScraper:
    def __init__(self):
        # Instantiate options
        options = webdriver.ChromeOptions()
        # Run browser in headless mode
        options.headless = True
        # Instantiate driver
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
   
    # Function for waiting to load the url
    @staticmethod
    def wait(seconds):
        time.sleep(seconds)

    # Function for scraping data
    @classmethod
    def scrape_quotes(self, url, output_file):
        # Getting url
        self.driver.get(url)
        # Loop until there is 'next' button
        while True:
            self.wait(30)
            # Opening json file
            with open(output_file, 'a') as f:
                # Select elements by class name
                elements = self.driver.find_elements(By.CLASS_NAME, 'quote')
                # Loop for quotes
                for quote_element in elements:
                    text = quote_element.find_element(By.CLASS_NAME, 'text').text
                    author = quote_element.find_element(By.CLASS_NAME, 'author').text
                    tags = [tag.text for tag in quote_element.find_elements(By.CLASS_NAME, 'tag')]
                    # Saving individual quote
                    quote = {
                        'text': text,
                        'by': author,
                        'tags': tags
                    }
                    # Saving in json file
                    json.dump(quote, f)
                    f.write('\n')
                # Clicking next button if possible
                try:
                    next_button = self.driver.find_element(By.XPATH, '/html/body/div/nav/ul/li/a')
                    next_button.click()
                except NoSuchElementException:
                    break

    # Qutting page
    def quit(self):
        self.driver.quit()

# Main
def main():
    output_file = os.getenv("OUTPUT_FILE")
    url = os.getenv("INPUT_URL")
    scraper = QuoteScraper()
    quotes = scraper.scrape_quotes(url, output_file)
    scraper.quit()
    print(f"Scraping completed. Quotes saved to {output_file}")


if __name__ == '__main__':
    main()