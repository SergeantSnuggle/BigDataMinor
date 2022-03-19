#https://www.datacamp.com/community/tutorials/amazon-web-scraping-using-beautifulsoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import re
import time
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

no_pages = 2

#https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg=1%27

def get_data(pageNo):  
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    r = requests.get('https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_'+str(pageNo)+'?ie=UTF8&pg='+str(pageNo), headers=headers)#, proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content)
    #print(soup)

    alls = []
    for d in soup.findAll('div', attrs={'class':'a-section a-spacing-none aok-relative'}):
        #print(d)
        name = d.find('span', attrs={'class':'zg-text-center-align'})
        n = name.find_all('img', alt=True)
        #print(n[0]['alt'])
        author = d.find('a', attrs={'class':'a-size-small a-link-child'})
        rating = d.find('span', attrs={'class':'a-icon-alt'})
        users_rated = d.find('a', attrs={'class':'a-size-small a-link-normal'})
        price = d.find('span', attrs={'class':'p13n-sc-price'})

        all1=[]

        if name is not None:
            #print(n[0]['alt'])
            all1.append(n[0]['alt'])
        else:
            all1.append("unknown-product")

        if author is not None:
            #print(author.text)
            all1.append(author.text)
        elif author is None:
            author = d.find('span', attrs={'class':'a-size-small a-color-base'})
            if author is not None:
                all1.append(author.text)
            else:
                all1.append('0')

        if rating is not None:
            #print(rating.text)
            all1.append(rating.text)
        else:
            all1.append('-1')

        if users_rated is not None:
            #print(price.text)
            all1.append(users_rated.text)
        else:
            all1.append('0')

        if price is not None:
            #print(price.text)
            all1.append(price.text)
        else:
            all1.append('0')
        alls.append(all1)
    return alls



results = []
for i in range(1, no_pages+1):
    results.append(get_data(i))
flatten = lambda l: [item for sublist in l for item in sublist]
df = pd.DataFrame(flatten(results),columns=['Book Name','Author','Rating','Customers_Rated', 'Price'])
df.to_csv('amazon_products.csv', index=False, encoding='utf-8')

#Reading CSV File

#Now let's load the CSV file you created and save in the above cell. Again, this is an optional step; you could even use the dataframe df directly and ignore the below step.

df = pd.read_csv("amazon_products.csv")
df.shape

df.head(5)

#From the customers_rated column, remove the comma.

df['Rating_clean'] = df['Rating'].apply(lambda x: x.split()[0])
df['Rating_clean'] = pd.to_numeric(df['Rating_clean'])

#From the price column, remove the rupees symbol, comma, and split it by dot.
df["Price_clean"] = df["Price"].str.replace('₹', '')

df["Price_clean"] = df["Price_clean"].str.replace(',', '')
df['Price_clean'] = df['Price_clean'].apply(lambda x: x.split('.')[0])
df['Price_clean'] = df['Price_clean'].astype(int)

df["Customers_Rated_clean"] = df["Customers_Rated"].str.replace(',', '')

df['Customers_Rated_clean'] = pd.to_numeric(df['Customers_Rated_clean'], errors='ignore')

df_clean=df.drop(['Rating','Price','Customers_Rated'], axis=1)

df_clean.head(5)
df_clean.rename(columns={'Rating_clean':'Rating', 'Price_clean':'Price','Customers_Rated_clean':'Customers_Rated'}, inplace = True)

df_clean.dtypes

df_clean.replace(str(0), np.nan, inplace=True)
df_clean.replace(0, np.nan, inplace=True)

count_nan = len(df_clean) - df_clean.count()

count_nan

data = df_clean.sort_values(["Price"], axis=0, ascending=False)[:15]
data

import plotly.express as px

fig = px.bar(data, x='Author', y='Price')
fig.show()


#Let's find out which authors have the top-rated books and 
# which books of those authors are top rated. 
# However, while finding this out, you would filter out those authors 
# in which less than 1000 customers rated.

# OLD SKOOL
data = df_clean[df_clean['Customers_Rated'] > 1000]

# NEW KID ON THE BLOCK
data=df_clean.loc[lambda df: df['Customers_Rated'] > 1000]
data = data.sort_values(['Rating'],axis=0, ascending=False)[:15]

fig = px.bar(data, x='Book Name', y='Rating')
fig.show()