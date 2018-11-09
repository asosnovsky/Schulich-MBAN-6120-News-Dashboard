import os
import json
import urllib

from random import sample, randint
from flask import Flask, render_template, jsonify
from api import newsapi
from api.newsapi.util import dict_factory

BASE_FOLDER = os.path.dirname(__file__)

app = Flask(__name__, static_folder=os.path.join(BASE_FOLDER, "static"))

SENTIMENT_TABLE = """
    SELECT 
        obj_id,
        topic,
        overall_sentiment,
        CASE 
            WHEN overall_sentiment <= -0.25 THEN "Very Negative"
            WHEN overall_sentiment <= 0 THEN "Negative"
            WHEN overall_sentiment <= 0.25 THEN "Positive"
            WHEN overall_sentiment > 0.25 THEN "Very Positive"
        END sentiment_state
    FROM article_sentiment
"""

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

@app.route("/data/nltk/newsfeed/<topic>/<scale>")
def route_data_nltk_newsfeed(topic: str, scale: str):
    return jsonify(newsapi.query_db(f"""
        SELECT 
            s.sentiment_state,
            a.*
        FROM
        (
            {SENTIMENT_TABLE}
            WHERE topic = ?
        ) AS s
        LEFT JOIN articles AS a ON a.obj_id=s.obj_id
        WHERE s.sentiment_state = ?
        ORDER BY a.publishedAt DESC
        LIMIT 10
    """, topic, scale))

@app.route("/data/nltk/sentiment-timeseries/<topic>")
def route_data_nltk_timeseries(topic: str):
    return jsonify(newsapi.query_db(f"""
        SELECT 
            strftime("%Y-%m-%d %H:00", a.publishedAt) AS date,
            s.sentiment_state,
            COUNT() as count
            FROM
            (
            {SENTIMENT_TABLE}
                WHERE topic = ?
            ) AS s
            LEFT JOIN articles AS a ON a.obj_id=s.obj_id
            GROUP BY 
                s.sentiment_state, 
                DATE(a.publishedAt),
                strftime("%H", a.publishedAt)
            ORDER BY a.publishedAt ASC
    """, topic))

@app.route("/data/nltk/counts/<topic>")
def route_data_nltk_counts(topic: str):
    output_data = {
        "Very Positive": 0,
        "Positive": 0,
        "Negative": 0,
        "Very Negative": 0,
    }

    data = newsapi.query_db(f"""
        SELECT 
            a.topic,
            s.sentiment_state,
            COUNT() AS count,
            a.publishedAt
        FROM
        (
            {SENTIMENT_TABLE}
            WHERE topic=?
        ) AS s
        LEFT JOIN articles AS a ON a.obj_id=s.obj_id
        GROUP BY s.sentiment_state
    """, topic)

    total = 0
    for row in data:
        total += row['count']
        output_data[row['sentiment_state']] = row['count']

    return jsonify([
        { "word": word, "count": count, "percent": round(100*count/total, 1) }
        for word, count in output_data.items()
    ])

if __name__ == "__main__":
    app.run(port="8080", debug=True)