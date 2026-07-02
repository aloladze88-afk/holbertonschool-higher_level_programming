#!/usr/bin/python3
"""
Flask application that displays product data from JSON or CSV files.
"""

import csv
import json
import os
from flask import Flask, render_template, request

app = Flask(__name__)


def read_json_file():
    """
    Read product data from products.json.
    """
    file_path = os.path.join(os.path.dirname(__file__), "products.json")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def read_csv_file():
    """
    Read product data from products.csv.
    """
    file_path = os.path.join(os.path.dirname(__file__), "products.csv")
    products = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            products.append({
                "id": int(row["id"]),
                "name": row["name"],
                "category": row["category"],
                "price": float(row["price"])
            })

    return products


@app.route("/products")
def products():
    """
    Display products from JSON or CSV, optionally filtered by id.
    """
    source = request.args.get("source")
    product_id = request.args.get("id")

    if source == "json":
        product_list = read_json_file()
    elif source == "csv":
        product_list = read_csv_file()
    else:
        return render_template(
            "product_display.html",
            products=[],
            error="Wrong source"
        )

    if product_id is not None:
        try:
            product_id = int(product_id)
        except ValueError:
            return render_template(
                "product_display.html",
                products=[],
                error="Product not found"
            )

        product_list = [
            product for product in product_list
            if product["id"] == product_id
        ]

        if not product_list:
            return render_template(
                "product_display.html",
                products=[],
                error="Product not found"
            )

    return render_template(
        "product_display.html",
        products=product_list,
        error=None
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
