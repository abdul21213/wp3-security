import json
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "Data", "database.db")

def init_database():
    create_taxonomy_table()
    create_test_table()
    insert_into_test_table()
    create_leerling_table()
    insert_into_leerling_table()
    insert_into_taxonomy()

def get_taxonomy_by_leerling(leerling_id):
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row  
    cur = con.cursor()

    cur.execute("""
        SELECT
            snapshot_at,
            test_id,
            leerdoel_id,
            level,
            kennen,
            kunnen,
            confidence
        FROM taxonomy
        WHERE leerling_id = ?
        ORDER BY snapshot_at DESC
    """, (leerling_id,))

    rows = cur.fetchall()
    con.close()
    return rows

def get_leerling_voornaam_by_id(leerling_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT voornaam FROM leerling WHERE leerling_id = ?",
        (leerling_id,)
    )

    result = cur.fetchone()
    conn.close()

    return result[0]

def insert_into_taxonomy():
    with open("Data/data-sample-small.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    snapshots_set = set()

    for entry in data["entries"]:
        student_id = entry["student"]["id"]
        subject_id = entry["subject"]["id"] 

        for learning_goal in entry["learningGoals"]:
            learning_goal_id = learning_goal["id"]
            for snapshot in learning_goal["snapshots"]:
                snapshot_at = snapshot["at"]
                snapshot_test_id = snapshot["source"]["id"]
                for score in snapshot["taxonomy"]:
                    level = score["level"]
                    kennen = score["kennen"]
                    kunnen = score["kunnen"]
                    confidence = score["confidence"]
                    snapshot_to_insert = (student_id, subject_id, learning_goal_id, snapshot_at, snapshot_test_id, level, kennen, kunnen, confidence)
                    snapshots_set.add(snapshot_to_insert)

    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()

    cur.executemany("""
    INSERT OR REPLACE INTO taxonomy (
        leerling_id,
        vak_id,
        leerdoel_id,
        snapshot_at,
        test_id,
        level,
        kennen,
        kunnen,
        confidence
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    snapshots_set)

    con.commit()
    con.close()

def create_leerling_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS leerling (
            leerling_id INTEGER PRIMARY KEY,
            voornaam TEXT NOT NULL,
            achternaam TEXT,
            klas_id INTEGER
        )
    """)

    conn.commit()
    conn.close()

def insert_into_leerling_table():
    with open("Data/data-sample-small.json", "r", encoding="utf-8") as file:
        data = json.load(file)
   
    leerling_set = set()

    for entry in data["entries"]:
        student = entry["student"]
        leerling = (student["id"], student["name"])
        leerling_set.add(leerling)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.executemany(
        "INSERT OR IGNORE INTO leerling (leerling_id, voornaam) VALUES (?, ?)",
        leerling_set
    )

    conn.commit()
    conn.close()


def insert_into_test_table():
    with open("Data/data-sample-small.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    test_set = set()

    for entry in data["entries"]:
        for goal in entry["learningGoals"]:
            for snapshot in goal["snapshots"]:
                source = snapshot["source"]
                test = (source["id"],source["type"], entry["subject"]["id"])
                test_set.add(test)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.executemany(
        "INSERT OR IGNORE INTO test (test_id, type, vak_id) VALUES (?, ?, ?)",
        test_set
    )

    conn.commit()
    conn.close()


def create_taxonomy_table():
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")

    cur = con.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS taxonomy (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    leerling_id INTEGER NOT NULL,
                    vak_id INTEGER NOT NULL,
                    leerdoel_id TEXT NOT NULL,

                    snapshot_at TEXT NOT NULL,

                    test_id TEXT NOT NULL,     
                    level TEXT NOT NULL,

                    kennen REAL NOT NULL,
                    kunnen REAL NOT NULL,
                    confidence REAL NOT NULL,

                    UNIQUE (
                        leerling_id,
                        vak_id,
                        leerdoel_id,
                        snapshot_at,
                        test_id,
                        level
                    ),

                    FOREIGN KEY (leerling_id) REFERENCES leerling(leerling_id),
                    FOREIGN KEY (vak_id) REFERENCES vak(vak_id),
                    FOREIGN KEY (test_id,vak_id) REFERENCES test(test_id, vak_id),
                    FOREIGN KEY (leerdoel_id) REFERENCES leerdoel(leerdoel_id)
                )
                """)

    con.commit() 
    con.close()

def create_test_table():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS test (
            test_id TEXT NOT NULL,
            type TEXT NOT NULL,
            vak_id INTEGER NOT NULL,
            PRIMARY KEY (test_id, vak_id),
            FOREIGN KEY (vak_id) REFERENCES vak(vak_id)
        )
    """)

    conn.commit()
    conn.close()



def get_or_create_taxonomie(cursor, naam, volgorde):
    cursor.execute(
        "SELECT taxonomie_id FROM taxonomieniveau WHERE naam = ?",
        (naam,)
    )
    row = cursor.fetchone()
    if row:
        return row[0]

    cursor.execute(
        "INSERT INTO taxonomieniveau (naam, volgorde) VALUES (?, ?)",
        (naam, volgorde)
    )
    return cursor.lastrowid


def get_or_create_kernwoord(cursor, woord):
    cursor.execute(
        "SELECT kernwoord_id FROM kernwoord WHERE woord = ?",
        (woord,)
    )
    row = cursor.fetchone()
    if row:
        return row[0]

    cursor.execute(
        "INSERT INTO kernwoord (woord) VALUES (?)",
        (woord,)
    )
    return cursor.lastrowid

def get_or_create_dataset(cursor, leerling_id, vak_id):
    cursor.execute(
        "SELECT dataset_id FROM dataset WHERE leerling_id = ? AND vak_id = ?",
        (leerling_id, vak_id)
    )
    row = cursor.fetchone()
    if row:
        return row[0]

    cursor.execute(
        "INSERT INTO dataset (leerling_id, vak_id) VALUES (?, ?)",
        (leerling_id, vak_id)
    )
    return cursor.lastrowid

def get_or_create_snapshot(cursor, leerdoel_id, dataset_id, datum, bron, bron_id):
    cursor.execute("""
        SELECT snapshot_id
        FROM snapshot
        WHERE leerdoel_id = ?
          AND dataset_id = ?
          AND datum = ?
          AND bron = ?
          AND bron_id = ?
    """, (leerdoel_id, dataset_id, datum, bron, bron_id))

    row = cursor.fetchone()
    if row:
        return row[0]

    cursor.execute("""
        INSERT INTO snapshot (leerdoel_id, dataset_id, datum, bron, bron_id)
        VALUES (?, ?, ?, ?, ?)
    """, (leerdoel_id, dataset_id, datum, bron, bron_id))

    return cursor.lastrowid

# JSON lezen
def import_json_into_db():
    with open("Data/data-sample-small.json", "r", encoding="utf-8") as file:
        data = json.load(file)


    # Database verbinden

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for entry in data["entries"]:
        # Leerling en vak opslaan
        student = entry["student"]
        subject = entry["subject"]

        cursor.execute("""
            INSERT OR IGNORE INTO leerling (leerling_id, voornaam, achternaam, klas_id)
            VALUES (?, ?, ?, ?)
        """, (
            student["id"],
            student["name"],
            "",
            None
        ))

        cursor.execute("""
            INSERT OR IGNORE INTO vak (vak_id, naam)
            VALUES (?, ?)
        """, (
            subject["id"],
            subject["name"]
        ))

        # Taxonomieniveaus opslaan
        taxonomy_ids = {}
        for index, level_name in enumerate(entry["taxonomyScale"]):
            tax_id = get_or_create_taxonomie(cursor, level_name, index)
            taxonomy_ids[level_name] = tax_id

        # Dataset (leerling, vak)
        dataset_id = get_or_create_dataset(
            cursor,
            student["id"],
            subject["id"]
        )

        # Leerdoelen, kernwoorden, snapshots en scores
        for lg in entry["learningGoals"]:
            leerdoel_id = lg["id"]
            titel = lg["title"]

            cursor.execute("""
                INSERT OR IGNORE INTO leerdoel (leerdoel_id, titel, vak_id)
                VALUES (?, ?, ?)
            """, (
                leerdoel_id,
                titel,
                subject["id"]
            ))

            # Kernwoorden + koppeltabel
            for kw in lg.get("keywords", []):
                kw_id = get_or_create_kernwoord(cursor, kw)
                cursor.execute("""
                    INSERT OR IGNORE INTO leerdoel_kernwoord (leerdoel_id, kernwoord_id)
                    VALUES (?, ?)
                """, (
                    leerdoel_id,
                    kw_id
                ))

            # Snapshots en scores
            for snap in lg.get("snapshots", []):
                datum = snap["at"]
                bron = snap["source"]["type"]
                bron_id = snap["source"]["id"]

                snapshot_id = get_or_create_snapshot(
                    cursor,
                    leerdoel_id,
                    dataset_id,
                    datum,
                    bron,
                    bron_id
                )

                for t in snap.get("taxonomy", []):
                    tax_id = taxonomy_ids[t["level"]]

                    cursor.execute("""
                        SELECT 1
                        FROM score
                        WHERE snapshot_id = ?
                        AND taxonomie_id = ?
                    """, (snapshot_id, tax_id))

                    exists = cursor.fetchone()
                    if not exists:
                        cursor.execute("""
                            INSERT INTO score
                            (kennen, kunnen, confidence, taxonomie_id, snapshot_id)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            t["kennen"],
                            t["kunnen"],
                            t["confidence"],
                            tax_id,
                            snapshot_id
                        ))

    conn.commit()
    conn.close()