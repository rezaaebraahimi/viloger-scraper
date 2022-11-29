from flask import Flask, render_template

app = Flask(__name__)

from requests_html import HTMLSession
sesssion = HTMLSession()
r = sesssion.get("https://vitalik.ca/")

r.html.render(timeout=10000 ,scrolldown=5)

viqoulik= r.html.find('h3')
articlelist = []
@app.route("/" , methods = ["POST", "GET"])
def index():
    for item in viqoulik:
        try:
            article = item.find('a',first=True)
            title = article.text 
            link = article.absolute_links
            articles = {
                "title" : title,
                "link" : link
            }
            articlelist.append(articles)
            return render_template("index.html", title=title, link=link, item=item, viqoulik=viqoulik )
        except:
            pass
app.run(host="0.0.0.0")