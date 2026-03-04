from flask import Flask, render_template, request
import sqlite3
import os
from Data.queries.docent import get_klassen, get_leerlingen, get_leerdoel_overzicht, get_leerling_leerdoel_overzicht
from Data.queries.student import get_vakken, get_leerdoelen

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

    vakken = get_vakken(conn, leerling_id)

    vak_id = request.args.get("vak_id", type=int)
    if vak_id is None and vakken:
        vak_id = vakken[0]["vak_id"]

    leerdoelen = []

    if vak_id is not None:
        resultaten = get_leerdoelen(conn, leerling_id, vak_id)

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

    return render_template(
        "dashboard-student.html",
        vakken=vakken,
        gekozen_vak_id=vak_id,
        leerdoelen=leerdoelen
    )


@app.route("/dashboard-docent")
def docent():
    docent_id = 1  # tijdelijk hardcoded

    conn = get_db_connection()

    klassen = get_klassen(conn, docent_id)

    klas_id = request.args.get("klas_id", type=int)
    leerling_id = request.args.get("leerling_id", type=int)  # NIEUW
    
    if klas_id is None and klassen:
        klas_id = klassen[0]["klas_id"]

    leerlingen = []
    leerdoel_overzicht = []
    geselecteerde_leerling = None  # NIEUW
    
    if klas_id is not None:
        leerlingen = get_leerlingen(conn, klas_id)
        
        if leerling_id is not None:
            leerdoel_overzicht = get_leerling_leerdoel_overzicht(conn, leerling_id)
            geselecteerde_leerling = next((l for l in leerlingen if l["leerling_id"] == leerling_id), None)
        else:
            leerdoel_overzicht = get_leerdoel_overzicht(conn, klas_id)

    conn.close()

    return render_template(
        "dashboard-docent.html",
        klassen=klassen,
        gekozen_klas_id=klas_id,
        leerlingen=leerlingen,
        leerdoel_overzicht=leerdoel_overzicht,
        geselecteerde_leerling=geselecteerde_leerling  # NIEUW
    )


if __name__ == "__main__":
    app.run(debug=True)
