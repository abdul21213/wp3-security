from typing import List
import sqlite3


def get_klassen(conn: sqlite3.Connection, docent_id: int) -> List[sqlite3.Row]:
    if conn is None:
        return []

    cur = conn.cursor()
    cur.execute(
        """
        SELECT klas_id, naam
        FROM klas
        WHERE docent_id = ?
        ORDER BY naam
        """,
        (docent_id,),
    )
    return cur.fetchall()


def get_leerlingen(conn: sqlite3.Connection, klas_id: int) -> List[sqlite3.Row]:
    if conn is None or klas_id is None:
        return []

    cur = conn.cursor()
    cur.execute(
        """
        SELECT leerling_id, voornaam, achternaam
        FROM leerling
        WHERE klas_id = ?
        ORDER BY achternaam, voornaam
        """,
        (klas_id,),
    )
    return cur.fetchall()
