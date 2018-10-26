import os

from flask import Flask, render_template, jsonify
from api import newsapi

BASE_FOLDER = os.path.dirname(__file__)

app = Flask(__name__, static_folder=os.path.join(BASE_FOLDER, "static"))

@app.route("/")
def route_index():
    return render_template("index.html")

@app.route("/data/<topic>")
def route_data(topic: str):
    return jsonify(newsapi.query_db(f"""
        SELECT * FROM articles 
        WHERE topic = ?;
    """, topic))

if __name__ == "__main__":
    app.run(port="8080", debug=True)