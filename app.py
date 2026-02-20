from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "Data", "database.db")  # <-- Data map!

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login_docent")
def login_docent():
    return render_template("login_docent.html")

@app.route("/login_student")
def login_student():
    return render_template("login_student.html")

@app.route("/dashboard-student")
def student():
    leerling_id = 1  # tijdelijk hardcoded

    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT l.leerdoel_id,
           l.titel,
           AVG((sc.kennen + sc.kunnen) / 2.0) AS gemiddelde
    FROM leerdoel l
    JOIN snapshot sn ON sn.leerdoel_id = l.leerdoel_id
    JOIN dataset d ON sn.dataset_id = d.dataset_id
    JOIN score sc ON sc.snapshot_id = sn.snapshot_id
    WHERE d.leerling_id = ?
    AND sn.snapshot_id = (
        SELECT sn2.snapshot_id
        FROM snapshot sn2
        JOIN dataset d2 ON sn2.dataset_id = d2.dataset_id
        WHERE sn2.leerdoel_id = l.leerdoel_id
        AND d2.leerling_id = ?
        ORDER BY sn2.datum DESC
        LIMIT 1
    )
    GROUP BY l.leerdoel_id
    """

    cur.execute(query, (leerling_id, leerling_id))
    resultaten = cur.fetchall()

    leerdoelen = []
    for r in resultaten:
        score = r["gemiddelde"] or 0

        if score >= 0.75:
            status, color = "Sterk", "success"
        elif score >= 0.5:
            status, color = "Voldoende", "warning"
        else:
            status, color = "Zwak", "danger"

        leerdoelen.append({
            "titel": r["titel"],
            "score": round(score * 100),
            "status": status,
            "color": color
        })

    conn.close()
    return render_template("dashboard-student.html", leerdoelen=leerdoelen)

@app.route("/dashboard-docent")
def docent():
    return render_template("dashboard-docent.html")


if __name__ == "__main__":
    app.run(debug=True)
