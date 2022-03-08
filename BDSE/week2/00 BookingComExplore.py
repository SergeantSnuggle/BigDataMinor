import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.booking.com/city/nl/amsterdam.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaKkBiAEBmAEJuAEKyAEF2AEB6AEB-AEOiAIBqAIDuAKw16_5BcACAdICJDcxNmNmNDFkLTJhMWItNGU1NS1iZGI3LWViMzFjMGM1YzRjYdgCBuACAQ;sid=20b5be27c89dbccc8938e75b2a2637d9;inac=0&'

getPage = requests.get(url) 
   
soup = BeautifulSoup(getPage.text, 'html.parser') 

item=soup.findAll('div', class_="sr__card")[0] 
hotelName = item.find('span', class_="bui-card__title").text 
print(hotelName)

hotelCity=item.find('a')
print(hotelCity)

hotelCity2=item.find('p',class_="bui-card__subtitle").text 
print(hotelCity2)





