from flask import Flask, render_template
from requests_html import HTMLSession
import snscrape.modules.twitter as sntwitter




app = Flask(__name__)


query = "(from:vitalik.eth) since:2022-09-01"
tweets = []
limit = 10


sesssion = HTMLSession()
r = sesssion.get("https://vitalik.ca/")

r.html.render(timeout=10000 ,scrolldown=5)

viloger= r.html.find('h3')
@app.route("/" , methods = ["POST", "GET"])
def index():
    for item in viloger:
        try:
            article = item.find('a',first=True)
            title = article.text 
            link = article.absolute_links
        
            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                if len(tweets) == limit:
                    break
                else:    
                    tweets.append([tweet.date, tweet.user.username, tweet.content])
                         
            return render_template("index.html",title=title, link=link, item=item, viloger=viloger, tweets=tweets)    
        except:
            pass


if __name__ == '__main__':
    app.run()