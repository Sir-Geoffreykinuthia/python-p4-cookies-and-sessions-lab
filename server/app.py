#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# so this routes clears the session and we can run the session again
@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
# gets all the articles from the database and its also dispalyed in the front end
def index_articles():
    articles = Article.query.all()
    article_information =[article.to_dict() for article in articles]
    return jsonify(article_information), 200


@app.route('/articles/<int:id>')
def show_article(id):
# the session allowing to set limit to the number we want viewd 
    session ["page_views"]=session.get("page_views", 0) +1
    if session ["page_views"] <= 3:
        article = Article.query.get(id)
        if article:
            return jsonify ({
                "id": article.id,
                "title": article.title,
                "content": article.content
            }),200
        else:
            return {"Message" : "404: Article not found."}, 404
    else:
        return {"Message" : "Maximum pageview limit reached"},401

if __name__ == '__main__':
    app.run(port=5555)





# flask db init
# flask db upgrade 
# python seed.py