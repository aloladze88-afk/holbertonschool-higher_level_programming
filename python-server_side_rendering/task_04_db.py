#!/usr/bin/python3
"""
Flask application that displays product data from JSON, CSV, or SQLite.
"""

import csv
import json
import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)


def create_database():
    """
    Create and populate the SQLite database if needed.
    """
    file_path = os.path.join(os.path.dirname(__file__), "products.db")

    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO Products (id, name, category, price)
        VALUES
        (1, 'Laptop', 'Electronics', 799.99),
        (2, 'Coffee Mug', 'Home Goods', 15.99)
    """)

    conn.commit()
    conn.close()


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


def read_sql_database():
    """
    Read product data from products.db.
    """
    create_database()

    file_path = os.path.join(os.path.dirname(__file__), "products.db")

    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, category, price FROM Products")
    rows = cursor.fetchall()

    conn.close()

    products = []

    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "price": row[3]
        })

    return products


@app.route("/products")
def products():
    """
    Display products from JSON, CSV, or SQLite.

    The source is chosen with the source query parameter.
    The product can optionally be filtered by id.
    """
    source = request.args.get("source")
    product_id = request.args.get("id")

    try:
        if source == "json":
            product_list = read_json_file()
        elif source == "csv":
            product_list = read_csv_file()
        elif source == "sql":
            product_list = read_sql_database()
        else:
            return render_template(
                "product_display.html",
                products=[],
                error="Wrong source"
            )
    except Exception:
        return render_template(
            "product_display.html",
            products=[],
            error="Database error"
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
    create_database()
    app.run(debug=True, port=5000)