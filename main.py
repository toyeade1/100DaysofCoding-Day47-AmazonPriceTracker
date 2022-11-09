import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os

# Setting Fixed Variables

URL = 'https://camelcamelcamel.com/product/B0B1G5M31V'
TARGET_PRICE = 230
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

# Creating Get Request to gather the HTML script for the amazon webpage chosen

response = requests.get(headers=header, url=URL)
response.raise_for_status()
response = response.text


# Creating the Web Scraper

soup = BeautifulSoup(response, 'lxml')
amzn = soup.select('tbody tr td', class_='even')
row_id = []

# There was some issue drawing out the specific table data needed so I brute forced it.

for row in amzn:
    row_id.append(row.getText().replace('\n', ''))

list_price_camel = (row_id[74]).replace('$', '')
list_price_camel = float(list_price_camel)
brand_name = row_id[68]
model_num = row_id[70]

if list_price_camel <= TARGET_PRICE:
    my_email = os.environ.get(['my_email'])
    my_password = os.environ.get(['my_password'])

    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=my_email,
                            msg=f'Subject:{brand_name} sale!! \n\n Hurry, {brand_name}-{model_num} is below your target price of {TARGET_PRICE}. Buy Now !!')