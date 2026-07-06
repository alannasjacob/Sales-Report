from flask import Flask, render_template
import sqlite3
import json

app = Flask(__name__)

DATABASE = "mobile_shop.db"


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