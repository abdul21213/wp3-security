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


def get_leerling_leerdoel_overzicht(conn: sqlite3.Connection, leerling_id: int) -> List[dict]:
    if conn is None or leerling_id is None:
        return []

    cur = conn.cursor()
    query = """
    SELECT l.leerdoel_id,
           l.titel,
           v.naam AS vak_naam,
           AVG((sc.kennen + sc.kunnen) / 2.0) AS gemiddelde
    FROM leerdoel l
    JOIN snapshot sn ON sn.leerdoel_id = l.leerdoel_id
    JOIN dataset d ON sn.dataset_id = d.dataset_id
    JOIN score sc ON sc.snapshot_id = sn.snapshot_id
    JOIN vak v ON v.vak_id = d.vak_id
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
    GROUP BY l.leerdoel_id, v.vak_id
    ORDER BY v.naam, gemiddelde DESC
    """

    cur.execute(query, (leerling_id, leerling_id))
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
            "vak_naam": r["vak_naam"],
            "score": round(score * 100),
            "status": status,
            "color": color
        })

    return leerdoel_overzicht


def get_leerling_taxonomie_scores(conn: sqlite3.Connection, leerling_id: int) -> List[sqlite3.Row]:
    if conn is None or leerling_id is None:
        return []

    cur = conn.cursor()
    cur.execute(
        """
        SELECT level,
               snapshot_at,
               AVG((kennen + kunnen) / 2.0) AS gemiddelde
        FROM taxonomy
        WHERE leerling_id = ?
        GROUP BY level, snapshot_at
        ORDER BY level, snapshot_at DESC
        """,
        (leerling_id,),
    )
    return cur.fetchall()

def get_leerling_gemiddelden_per_klas(conn: sqlite3.Connection, klas_id: int) -> List[dict]:
    if conn is None or klas_id is None:
        return []

    cur = conn.cursor()
    cur.execute(
        """
        SELECT leer.leerling_id,
               leer.voornaam,
               leer.achternaam,
               AVG((sc.kennen + sc.kunnen) / 2.0) AS gemiddelde
        FROM leerling leer
        JOIN dataset d ON d.leerling_id = leer.leerling_id
        JOIN snapshot sn ON sn.dataset_id = d.dataset_id
        JOIN score sc ON sc.snapshot_id = sn.snapshot_id
        WHERE leer.klas_id = ?
        GROUP BY leer.leerling_id
        ORDER BY gemiddelde DESC
        """,
        (klas_id,),
    )

    resultaten = cur.fetchall()
    leerlingen = []

    for r in resultaten:
        score = round((r["gemiddelde"] or 0) * 100)

        if score >= 75:
            status, color = "Sterk", "success"
        elif score >= 50:
            status, color = "Voldoende", "warning"
        else:
            status, color = "Zwak", "danger"

        naam = r["voornaam"]
        if r["achternaam"]:
            naam += " " + r["achternaam"]

        leerlingen.append({
            "leerling_id": r["leerling_id"],
            "naam": naam,
            "score": score,
            "status": status,
            "color": color
        })

    return leerlingen

def get_taxonomie_gemiddelden_per_klas(conn: sqlite3.Connection, klas_id: int) -> List[dict]:
    if conn is None or klas_id is None:
        return []

    cur = conn.cursor()
    cur.execute(
        """
        SELECT t.level,
               AVG((t.kennen + t.kunnen) / 2.0) AS gemiddelde
        FROM taxonomy t
        JOIN leerling leer ON leer.leerling_id = t.leerling_id
        WHERE leer.klas_id = ?
        GROUP BY t.level
        ORDER BY gemiddelde DESC
        """,
        (klas_id,),
    )

    resultaten = cur.fetchall()
    niveaus = []

    for r in resultaten:
        score = round((r["gemiddelde"] or 0) * 100)

        if score >= 75:
            status, color = "Sterk", "success"
        elif score >= 50:
            status, color = "Voldoende", "warning"
        else:
            status, color = "Zwak", "danger"

        niveaus.append({
            "level": r["level"],
            "score": score,
            "status": status,
            "color": color
        })

    return niveaus
