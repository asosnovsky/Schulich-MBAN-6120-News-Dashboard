import os
import json
import urllib

from random import sample, randint
from flask import Flask, render_template, jsonify
from api import newsapi
from api.newsapi.util import dict_factory

BASE_FOLDER = os.path.dirname(__file__)

app = Flask(__name__, static_folder=os.path.join(BASE_FOLDER, "static"))

@app.route("/")
def route_index():
    return render_template("index.html")

@app.route("/data/topics")
def route_data():
    return jsonify(newsapi.query_db(f"""
        SELECT distinct topic FROM word_counts 
    """, mapping_function=lambda _, r: r[0]))

@app.route("/data/articles/<topic>")
def route_data_articles(topic: str):
    return jsonify(newsapi.query_db(""" 
        SELECT * FROM articles
        WHERE topic = ?
        ORDER BY publishedAt DESC
        LIMIT 10
        ;
    """, topic))

@app.route("/data/word-count/<topic>")
def route_data_word_count(topic: str):
    return jsonify(newsapi.query_db(""" 
        SELECT 
            word, 
            COUNT() as size
        FROM word_counts
        WHERE topic = ?
        GROUP BY topic, word
        HAVING size > 1
        LIMIT 200;
    """, topic))

@app.route("/data/nltk/counts/<topic>")
def route_data_nltk_counts(topic: str):
    mock_data = {
        "Positive": randint(50, 100),
        "Negative": randint(50, 100),
        "Neutral": randint(25, 50),
        "Other": randint(0, 10)
    }
    total = mock_data["Positive"] + mock_data['Negative'] + mock_data['Neutral'] + mock_data['Other']

    return jsonify([
        { "word": word, "count": count, "percent": round(100*count/total, 1) }
        for word, count in mock_data.items()
    ])

@app.route("/data/nltk/top_10/<topic>")
def route_data_nltk_top_10(topic: str):
    word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    response = urllib.request.urlopen(word_url)
    long_txt = response.read().decode()
    words = long_txt.splitlines()
    return jsonify({
        "positive": [
            { "word": sample(words, 1)[0], "size": 20 - j }
            for j in range(10)
        ],
        "negative": [
            { "word": sample(words, 1)[0], "size": 20 - j }
            for j in range(10)
        ],
        "neutral": [
            { "word": sample(words, 1)[0], "size": 20 - j }
            for j in range(10)
        ],
        "other": [
            { "word": sample(words, 1)[0], "size": 20 - j }
            for j in range(10)
        ],
    })

if __name__ == "__main__":
    app.run(port="8080", debug=True)