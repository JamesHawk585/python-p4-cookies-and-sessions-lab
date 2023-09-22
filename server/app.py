#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session, request
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


# An API endpoint at /clear is available to clear your session as needed.
@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass


# All lab instructions specify changes to @app.route('/articles/<int:id>
@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    # [x] For every request to /articles/<int:id>, increment the value of session['page_views'] by 1.
    if 'page_views' not in session:
        session['page_views'] = 0
    session['page_views'] += 1

    if session['page_views'] <= 3:
        article = Article.query.get(id)

        return jsonify({
        'session': {
                'session_key': id,
                'session_value': session[id],
                'session_accessed': session.accessed,
        },
        'article': {
            'title': article.title,
            'content': article.content,
        },
        'cookies': [{cookie: request.cookies[cookie]}
                    for cookie in request.cookies]
        }), 200
    else: 
        return jsonify({
            'message': 'Maximum pageview limit reached'
        }), 401
    

    # [] If the user has viewed 3 or fewer pages, render a JSON response with the article data.
    # [] If the user has viewed more than 3 pages, render a JSON response including an error message {'message': 'Maximum pageview limit reached'}, and a status code of 401 unauthorized.

    # response = make_response(jsonify({
    #     'session': {
    #             'session_key': id,
    #             'session_value': session[id],
    #             'session_accessed': session.accessed,
    #     },
    #     'cookies': [{cookie: request.cookies[cookie]}
    #                 for cookie in request.cookies]
    # }), 200)
    
    # return response.set_cookie('page_views', str(session[id]))


if __name__ == '__main__':
    app.run(port=5555)
