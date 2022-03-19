# https://www.dataquest.io/blog/web-scraping-tutorial-python/

import requests

page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
page.status_code

page.content


from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')

print(soup.prettify())
# go down the long way

list(soup.children)

html = list(soup.children)[2]
html

list(html.children)

body = list(html.children)[3]
body

p = list(body.children)[1]
p.get_text()

# short cut
soup.find_all('p')

soup.find_all('p')[0].get_text()

# https:/forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168
page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")

soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")

print(seven_day)

forecast_items = seven_day.find_all(class_="tombstone-container")

tonight = forecast_items[2]
print(tonight.prettify())

period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()

print(period)
print(short_desc)
print(temp)

img = tonight.find("img")
desc = img['title']

print(desc)

period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]
print(periods)

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

print(short_descs)
print(temps)
print(descs)


import pandas as pd
weather = pd.DataFrame({
        "period": periods, 
        "short_desc": short_descs, 
        "temp": temps, 
        "desc":descs
    })
weather

weather=weather.assign(tmp_num = lambda x: x['temp'].str.extract('(\d+)'))
weather