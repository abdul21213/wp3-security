import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # /Data/queries
DATA_DIR = os.path.dirname(BASE_DIR)                           # /Data
DB_PATH = os.path.join(DATA_DIR, "database.db")                # /Data/database.db

DOCENT_VOORNAAM = "Docent"
DOCENT_ACHTERNAAM = "Dummy"
DOCENT_EMAIL = "dummy.docent@example.com"  # placeholder

KLAS_NAAM = "1A"


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO docent (voornaam, achternaam, email)
            VALUES (?, ?, ?)
            """,
            (DOCENT_VOORNAAM, DOCENT_ACHTERNAAM, DOCENT_EMAIL),
        )
        docent_id = cur.lastrowid

        cur.execute(
            """
            INSERT INTO klas (naam, docent_id)
            VALUES (?, ?)
            """,
            (KLAS_NAAM, docent_id),
        )
        klas_id = cur.lastrowid

        cur.execute(
            """
            UPDATE leerling
            SET klas_id = ?
            WHERE klas_id IS NULL
            """,
            (klas_id,),
        )
        updated = cur.rowcount

        conn.commit()

        print(f"DB gebruikt: {DB_PATH}")
        print(f"Docent aangemaakt: docent_id={docent_id}")
        print(f"Klas aangemaakt: klas_id={klas_id} ({KLAS_NAAM})")
        print(f"Leerlingen bijgewerkt (NULL -> {klas_id}): {updated}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()