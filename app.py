import os
from flask import Flask, render_template
from requests_html import HTMLSession
import snscrape.modules.twitter as sntwitter
from requests import *
import requests
from json import *

app  = Flask(__name__)


query = "(from:VitalikButerin) since:2022-09-01 -filter:replies"
tweets = []

query_2 = "vitalik buterin 'vitalik buterin' since:2022-09-01 -filter:links -filter:replies"
tweets_2 = []

sesssion = HTMLSession()
r = sesssion.get("https://vitalik.ca/")


viloger= r.html.find('h3')


@app.route("/" , methods=["POST", "GET"])
def index():
    for item in viloger:
        try:
            article = item.find('a',first=True)
            title = article.text 
            link = article.absolute_links
        
            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                if len(tweets) == 5:
                    break
                else:    
                    tweets.append([tweet.date, tweet.user.username, tweet.content])
            
            for tweet in sntwitter.TwitterSearchScraper(query_2).get_items():
                if len(tweets_2) == 3:
                    break
                else:    
                    tweets_2.append([tweet.date, tweet.user.username, tweet.content])
                    
                    
                    
            url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
            parameters = {'start':'2','limit':'1','convert':'USD'}

            headers = {'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '1d07af25-ee62-461c-8f28-82831753bf5d'}

            session = Session()
            session.headers.update(headers)
                        
            json = requests.get(url, params=parameters, headers=headers).json()
            coins = json["data"]
            for x in coins:
                symbol = x['symbol']
                price = "%.2f" % x['quote']['USD']['price']
                eth_price = f"{symbol}: \n{price}"
                             
            return render_template("index.html",title=title,
                                   link=link, item=item, viloger=viloger,
                                   tweets=tweets,tweets_2=tweets_2,eth_price=eth_price)    
        except:
            pass


if __name__ == "__main__":
    app.run(host:="0.0.0.0", port:=int(os.environ.get('PORT', 5000)))