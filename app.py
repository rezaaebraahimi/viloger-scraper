from flask import Flask, render_template
from requests_html import HTMLSession
import snscrape.modules.twitter as sntwitter


app = Flask(__name__)


query = "(from:VitalikButerin) since:2022-09-01 -filter:replies"
tweets = []

query_2 = "vitalik buterin 'vitalik buterin' since:2022-09-01 -filter:links -filter:replies"
tweets_2 = []

sesssion = HTMLSession()
r = sesssion.get("https://vitalik.ca/")

r.html.render(timeout=20,scrolldown=5)

viloger= r.html.find('h3')
@app.route("/" , methods = ["POST", "GET"])
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
                         
            return render_template("index.html",title=title, link=link, item=item, viloger=viloger, tweets=tweets,tweets_2=tweets_2)    
        except:
            pass


if __name__ == '__main__':
    app.run()