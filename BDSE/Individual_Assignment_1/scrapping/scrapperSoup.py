import re
from urllib.parse import quote

from bs4 import BeautifulSoup
import requests
import pandas as pd


def clean_review(hotel_review):

    review = str(hotel_review)
    review = review.replace("\n", " ")
    review = review.strip('[ ]')
    sep = 'Stayed'
    stripped = review.split(sep, 1)[0]

    return stripped


def clean_rating(rating):
    rating = rating.replace('\n', '')

    return float(rating)


def soup_scrapper_booking(url: str, num_of_pages=1, num_reviews_per_page=24):
    """
    Function for scrapping a booking.com/reviews site(works only on that specific site not the normal site

    :param url: The url of the website you want to scrape
    :param num_of_pages: Amount of pages you want to scrape
    :param num_reviews_per_page: number of reviews you want to scrape per page
    :return: returns a labelled dataframe of reviews.
    """
    if num_reviews_per_page > 24:
        num_reviews_per_page = 24

    review_list = []
    rating_list = []

    for page_number in range(num_of_pages):
        urlPage = url + "?page=" + str(page_number+1)
        page = requests.get(urlPage)
        soup = BeautifulSoup(page.content, 'html.parser')
        for reviews in range(num_reviews_per_page):
            review = clean_review(soup.findAll("div", class_="review_item_review_content")[reviews].get_text())
            rating = clean_rating(soup.findAll("span", class_="review-score-badge")[reviews + 1].get_text())

            review_list.append(review)
            rating_list.append(rating)

    dfReviews = pd.DataFrame(list(zip(rating_list, review_list)), columns=['Reviewer_Score', 'Review'])
    dfReviews["label"] = dfReviews['Reviewer_Score'].astype(float).apply(lambda x: 1 if x > 5.5 else 0)
    return dfReviews



