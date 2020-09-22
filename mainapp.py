import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import csv
import datetime
import decimal

companies = ['PD','ZUO','PINS','ZM','PVTL','DOCU','CLDR','RUN',]

base_url = "https://finance.yahoo.com/quote/"


def get_companies():
    for company in companies:
        companyname = yf.Ticker(company)
        filename = company
        hist = companyname.history(period="max")
        hist.to_csv(f"{filename}.csv")
        data = pd.read_csv(f'{filename}.csv')
        data['3day_before_change'] = None
        print(data)


def get_news():
    for company in companies:
        page = urllib.request.urlopen(base_url+company).read()
        soup = BeautifulSoup(page, features="html5lib")
        with open('%s_summary.csv' % company, 'w') as output_file:
            writer = csv.writer(output_file, delimiter=',')
            writer.writerow(['link', 'title'])
            for news_block in soup.find_all('li', attrs={"class", "js-stream-content Pos(r)"}):
                link = news_block.find('h3').get_text()
                title = urllib.parse.urljoin(base_url, news_block.find('a').get('href'))
                row = [link, title]
                writer.writerow(row)
                output_file.flush()
    print("Done")


if __name__ == "__main__":
    get_companies()
    get_news()
