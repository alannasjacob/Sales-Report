import os
from flask import Flask, render_template
import sqlite3
import psycopg2
import json

app = Flask(__name__)

DATABASE = "mobile_shop.db"
DATABASE_URL = os.getenv("DATABASE_URL")


@app.route("/customers")
def customers():

    conn = psycopg2.connect(DATABASE_URL)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT CustomerID,
               CustomerName,
               Phone,
               Email
        FROM Customers
        ORDER BY CustomerID;
    """)

    customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("customers.html", customers=customers)

@app.route("/")
def index():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Brand, SUM(TotalAmount)
        FROM Sales
        GROUP BY Brand
    """)

    rows = cursor.fetchall()

    conn.close()

    brands = [row[0] for row in rows]
    totals = [row[1] for row in rows]

    return render_template(
        "index.html",
        brands=json.dumps(brands),
        totals=json.dumps(totals)
    )

if __name__ == "__main__":
    app.run(debug=True)

