#!/usr/bin/env python3
"""Convert CSV data to JSON format."""

import csv
import json


def convert_csv_to_json(csv_file):
    """Convert a CSV file into a JSON file named data.json."""
    try:
        with open(csv_file, "r", encoding="utf-8") as file:
            data = list(csv.DictReader(file))

        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        return True

    except Exception:
        return False
