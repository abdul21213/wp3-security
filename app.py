from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import os
import Data.database as db
from services.progress import LEVELS, score_pct, kleurklasse
from collections import defaultdict
from Data.queries.docent import get_klassen, get_leerlingen, get_leerdoel_overzicht, get_leerling_leerdoel_overzicht
from Data.queries.student import get_vakken, get_leerdoelen, get_kernwoorden
from flask import jsonify
from Data.queries.student import get_student_progress

app = Flask(__name__)
app.secret_key = "geheimesleutel"

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

    if session.get("role") != "student":
        return redirect(url_for("login_student"))

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

@app.route("/resultaten-student")
def resultaten_student():
    leerling_id = 1
    voornaam = db.get_leerling_voornaam_by_id(leerling_id)

    vakken = db.get_all_vakken()  

    leerdoelen = db.get_all_leerdoelen()

    return render_template(
        "resultaten-student.html",
        voornaam=voornaam,
        vakken=vakken,
        leerdoelen=leerdoelen
    )

@app.route("/resultaten-student/fragment")
def resultaten_student_fragment():
    leerling_id = 1

    vak_id = request.args.get("vak_id", "")
    level = request.args.get("level", "")
    leerdoel_id = request.args.get("leerdoel", "")
    test_type = request.args.get("test_type", "")

    resultaten = db.get_taxonomy_joined_by_filters(
        leerling_id=leerling_id,
        vak_id=vak_id,
        level=level,
        leerdoel_id=leerdoel_id,
        test_type=test_type
    )

    per_level = defaultdict(list)
    for r in resultaten:
        per_level[r["level"]].append(r)

    level_cards = []

    levels_to_show = [level] if level else LEVELS

    for lvl in levels_to_show:
        rows = per_level[lvl]

        if not rows:
            continue

        latest_pct = score_pct(rows[0])

        delta = None
        if len(rows) > 1:
            delta = latest_pct - score_pct(rows[1])

        level_cards.append({
            "level": lvl,
            "has_data": True,
            "pct": latest_pct,
            "class": kleurklasse(latest_pct),
            "date": rows[0]["snapshot_at"],
            "delta": delta
        })

    return render_template(
        "resultaten-tabel.html",
        resultaten=resultaten,
        level_cards=level_cards
    )

@app.route("/dashboard-docent")
def docent():

    if session.get("role") != "docent":
        return redirect(url_for("login_docent"))

    return render_template("dashboard-docent.html")
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

@app.route("/set-role/<role>")
def set_role(role):
    session["role"] = role

    if role == "student":
        return redirect(url_for("student"))

    if role == "docent":
        return redirect(url_for("docent"))

    return redirect(url_for("index"))
@app.route("/api/progress")
def api_progress():
    leerling_id = 1  # tijdelijk hardcoded, net als in dashboard-student
    vak_id = request.args.get("vak_id", type=int) or 1

    conn = get_db_connection()
    data = get_student_progress(conn, leerling_id, vak_id)
    conn.close()

    # omzetten naar JSON
    data_json = [{"date": row["date"], "score": row["score"]} for row in data]
    return jsonify(data_json)


if __name__ == "__main__":
    db.init_database()
    app.run(debug=True)
