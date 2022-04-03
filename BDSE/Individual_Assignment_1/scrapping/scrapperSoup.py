import re
from urllib.parse import quote

from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_hotel_review(hotel_review):

    review = str(hotel_review)
    review = review.replace("\n", " ")
    review = review.strip('[ ]')
    sep = 'Stayed'
    stripped = review.split(sep, 1)[0]

    return stripped


def get_hotel_rating(rating):
    rating = rating.replace('\n', '')

    return float(rating)


def soup_scrapper_booking(url: str, num_of_reviews=20):
    review_list = []
    rating_list = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for x in range(num_of_reviews):
        review = get_hotel_review(soup.findAll("div", class_="review_item_review_content")[x].get_text())
        rating = get_hotel_rating(soup.findAll("span", class_="review-score-badge")[x + 1].get_text())

        review_list.append(review)
        rating_list.append(rating)

    df = pd.DataFrame(list(zip(rating_list, review_list)),
                      columns=['reviewer_score',  'review'])
    return df


df = soup_scrapper_booking("https://www.booking.com/reviews/nl/hotel/westcord-city-centre.en-gb.html?page=2")
