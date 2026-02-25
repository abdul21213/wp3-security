import json
import sqlite3

DB_PATH = "Data/database.db"



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
                    FOREIGN KEY (test_id) REFERENCES test(test_id),
                    FOREIGN KEY (leerdoel_id) REFERENCES leerdoel(leerdoel_id)
                )
                """)

    con.commit() 
    con.close()

def create_test_table():
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")

    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS test (
        test_id INTEGER PRIMARY KEY,              
        subject TEXT NOT NULL,
        date TEXT,                                
        type TEXT,
        kernwoord_id INTEGER NOT NULL,
        leerling_id INTEGER NOT NULL,
        taxonomy_id INTEGER,

        FOREIGN KEY (kernwoord_id) REFERENCES kernwoord(kernwoord_id),
        FOREIGN KEY (leerling_id) REFERENCES leerling(leerling_id),
        FOREIGN KEY (taxonomy_id) REFERENCES taxonomy(taxonomy_id)
    )
    """)

    con.commit()
    con.close()



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

create_taxonomy_table()
create_test_table()