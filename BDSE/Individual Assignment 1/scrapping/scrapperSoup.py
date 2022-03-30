from urllib.parse import quote

from bs4 import BeautifulSoup
import requests
import pandas as pd

def soup_scrapper_tui(test1, test2, test3):
    base_url = 'https://www.tui.nl/'
    hotel_url = 'papagayo-beach-hotel-509479326'
    section_url = ('/#beoordelingen')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; nl; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
        'Accept-Language': 'nl-NE'
    }

    website_url = base_url + hotel_url

    page = requests.get(website_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Retrieve number of review pages
    page_amount = int(soup.find('li', class_='last').get_text())

    review_list = []
    # loop trough every page
    for page_number in range(1, (page_amount+1)):

        # set url for next page
        page_url = base_url + hotel_url + section_url + str(page_number)

        try:
            page_url = requests.get(page_url)
            page_url.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        soup = BeautifulSoup(page_url.content, 'lxml')

        page_reviews = soup.find_all('article', itemprop='review')

        for review_index, review in enumerate(page_reviews):

            reviewscore = review.find('span', itemprop='ratingValue').get_text()
            reviewtext = review.find('p', itemprop='reviewBody').get_text()
            review_list.append([reviewtext, int(reviewscore)])

            reviewDf = pd.DataFrame(review_list, columns=["reviewtext", "reviewscore"])