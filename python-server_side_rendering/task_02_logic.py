#!/usr/bin/python3
"""
Flask application that renders a dynamic list of items from a JSON file.
"""

import json
import os
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    """Render the home page."""
    return render_template("index.html")


@app.route("/about")
def about():
    """Render the about page."""
    return render_template("about.html")


@app.route("/contact")
def contact():
    """Render the contact page."""
    return render_template("contact.html")


@app.route("/items")
def items():
    """Render the items page using data from items.json."""
    file_path = os.path.join(os.path.dirname(__file__), "items.json")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    items_list = data.get("items", [])

    return render_template("items.html", items=items_list)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
