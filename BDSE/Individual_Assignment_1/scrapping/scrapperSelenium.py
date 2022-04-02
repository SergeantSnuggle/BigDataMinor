from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# accepting cookies
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')


def selenium_scrapper_tripadvisor(link, numberOfPages):
    """
    A function to scrape data from a tripadvisor hotel review site.

    :param link: The link of the hotel you want to scrape reviews from
    :param numberOfPages: amount of pages you want to scrape from the given link(tripadvisor has 10 reviews per page)
    so amount of reviews scrapped will be x10
    :return: returns a dataframe of scrapped reviews
    """
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(link)
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept")]'))).click()

    scrapedReviews = []

    # change the value inside the range to save more or less reviews
    for i in range(0, numberOfPages):

        # expand the review
        time.sleep(2)

        container = driver.find_elements(by=By.XPATH, value="//div[@data-reviewid]")

        for j in range(len(container)):
            hotelname = driver.find_element(by=By.XPATH,
                                            value=".//h1[contains(@class, 'fkWsC b d Pn')]").text
            rating = container[j].find_element(by=By.XPATH,
                                          value=".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute(
                                        "class").split("_")[3]
            title = container[j].find_element(by=By.XPATH,
                                              value=".//div[contains(@data-test-target, 'review-title')]").text
            review = container[j].find_element(by=By.XPATH,
                                               value=".//div[contains(@class,'pIRBV')]").text.replace("\n", "  ")

            scrapedReviews.append([hotelname, title, review, rating])

        #Go to the next review page
        driver.find_element(by=By.XPATH, value='.//a[@class="ui_button nav next primary "]').click()

    scrapedReviews = pd.DataFrame(scrapedReviews, columns=['hotelname', 'title', 'review', 'rating'])
    driver.quit()
    print('Scrapping done, adding labels')
    scrapedReviews["label"] = scrapedReviews['rating'].astype(float).apply(lambda x: 1 if x > 30 else 0)

    return scrapedReviews

