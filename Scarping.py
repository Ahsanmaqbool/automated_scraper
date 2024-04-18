import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()
search_str = "binance"
Date_Range = "past_month"
section = "world"


def scrapper(keyword, Date_Range, scope):
    try:
        url = f'https://www.reuters.com/site-search/?query={keyword}&date={Date_Range}&section={scope}'
        driver.get(url)

        # Opening CSV file for writing
        with open('reuters_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Date', 'Content']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Find all the headlines
            headlines = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="search-results__list__2SxSK"]//span[@data-testid="Heading"]')))
            for headline in headlines:
                headline.click()  # Click on each headline
                # Extracting data
                title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h1[@data-testid="Heading"]'))).text
                date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//time//span[@class="date-line__date___kNbY"]'))).text
                content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="article-body__content__17Yit"]//div'))).text
                # Writing to CSV
                writer.writerow({'Title': title, 'Date': date, 'Content': content})
                # Going back to the search results page
                driver.back()

    except Exception as ex:
        print(f"An error occurred: {str(ex)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    scrapper(search_str, Date_Range, section)
