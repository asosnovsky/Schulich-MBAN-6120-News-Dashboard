import os
import json

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

@app.route("/data/word-count/<topic>")
def route_data_word_count(topic: str):
    return jsonify(newsapi.query_db(""" 
        SELECT 
            word, 
            COUNT() as size
        FROM word_counts
        WHERE topic = ?
        GROUP BY topic, word
        HAVING size > 1;
    """, topic))

@app.route("/data/sources/<topic>")
def route_data_sources(topic: str):
    def mapping_function(c, row):
        obj = dict_factory(c, row)
        json_source = json.loads(obj['source'])
        obj['source'] = json_source['name'] if json_source['name'] else json_source['id']
        return obj
    return jsonify(newsapi.query_db(""" 
        SELECT 
            topic, source, 
            COUNT() as size
        FROM articles
        WHERE topic = ?
        GROUP BY topic, source
        HAVING size > 2
    """, topic, mapping_function=mapping_function))

if __name__ == "__main__":
    app.run(port="8080", debug=True)