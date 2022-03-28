import pandas as pd
import requests
from bs4 import BeautifulSoup

citiesUrls = []
with open('bookingCom.txt') as webSet:
    for url in webSet:
        citiesUrls.append(url.replace('\n', ''))

scrapedAccommodations = []
for url in citiesUrls:
    # Check if page gives a response back
    getPage = requests.get(url) # 1
    statusCode = getPage.status_code # 2
    
    if(statusCode == 200): # 3
        soup = BeautifulSoup(getPage.text, 'html.parser') # 1

        for item in soup.findAll('div', class_="sr__card"): # 2
            hotelName = item.find('span', class_="bui-card__title").text # 3
            totalReviewsText = item.find('div', class_="bui-review-score__text").text # 4

            totalReviews = totalReviewsText.split(' ', 1)[0] # 5
            totalReviews = totalReviews.replace(',', '')
            scrapedAccommodations.append([hotelName, int(totalReviews)]) # 6

            accommodationsDF = pd.DataFrame(scrapedAccommodations, columns=['hotel_name', 'total_reviews'])

        print("Total Accommodations Scraped: ", len(scrapedAccommodations))
    else:
        print("Page doesn't respond")

accommodationsDF.head(10)



