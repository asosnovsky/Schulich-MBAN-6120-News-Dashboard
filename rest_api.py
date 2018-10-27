import os

from flask import Flask, render_template, jsonify
from api import newsapi

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

if __name__ == "__main__":
    app.run(port="8080", debug=True)