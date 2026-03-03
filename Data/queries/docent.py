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

# Sterke/Zwakke punten
def get_leerdoel_overzicht(conn: sqlite3.Connection, klas_id: int) -> List[dict]:

    if conn is None or klas_id is None:
        return []

    cur = conn.cursor()
    query = """
    SELECT l.leerdoel_id,
           l.titel,
           AVG((sc.kennen + sc.kunnen) / 2.0) AS gemiddelde
    FROM leerdoel l
    JOIN snapshot sn ON sn.leerdoel_id = l.leerdoel_id
    JOIN dataset d ON sn.dataset_id = d.dataset_id
    JOIN score sc ON sc.snapshot_id = sn.snapshot_id
    JOIN leerling leer ON leer.leerling_id = d.leerling_id
    WHERE leer.klas_id = ?
      AND sn.snapshot_id = (
          SELECT sn2.snapshot_id
          FROM snapshot sn2
          JOIN dataset d2 ON sn2.dataset_id = d2.dataset_id
          WHERE sn2.leerdoel_id = l.leerdoel_id
            AND d2.leerling_id = d.leerling_id
          ORDER BY sn2.datum DESC
          LIMIT 1
      )
    GROUP BY l.leerdoel_id
    ORDER BY gemiddelde DESC
    """
    
    cur.execute(query, (klas_id,))
    resultaten = cur.fetchall()
    
    leerdoel_overzicht = []
    for r in resultaten:
        score = r["gemiddelde"] or 0
        
        if score >= 0.75:
            status, color = "Sterk", "success"
        elif score >= 0.5:
            status, color = "Voldoende", "warning"
        else:
            status, color = "Zwak", "danger"
        
        leerdoel_overzicht.append({
            "titel": r["titel"],
            "score": round(score * 100),
            "status": status,
            "color": color
        })
    
    return leerdoel_overzicht
