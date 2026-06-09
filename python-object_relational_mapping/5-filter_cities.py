#!/usr/bin/python3
"""Lists all cities of a given state from a MySQL database."""

import sys
import MySQLdb


if __name__ == "__main__":
    db = MySQLdb.connect(
        host="localhost",
        port=3306,
        user=sys.argv[1],
        passwd=sys.argv[2],
        db=sys.argv[3]
    )

    cursor = db.cursor()

    query = """
        SELECT cities.name
        FROM cities
        JOIN states
        ON cities.state_id = states.id
        WHERE states.name = %s
        ORDER BY cities.id ASC
    """

    cursor.execute(query, (sys.argv[4],))

    rows = cursor.fetchall()
    cities = [row[0] for row in rows]

    print(", ".join(cities))

    cursor.close()
    db.close()
